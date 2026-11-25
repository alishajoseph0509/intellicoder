import time
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain.agents import create_agent

from agent.prompts import *
from agent.states import *
from agent.tools import (
    write_file, read_file, get_current_directory, list_files, init_project_root,
)

_ = load_dotenv()
init_project_root()

llm = ChatGroq(model="openai/gpt-oss-120b", max_retries=8)

def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    raw_resp = llm.invoke(
        architect_prompt(plan=str(plan))
    )

    from langchain_core.output_parsers import PydanticOutputParser

    parser = PydanticOutputParser(pydantic_object=TaskPlan)
    resp = parser.parse(raw_resp.content)
    if resp is None:
        raise ValueError("Planner did not return a valid response.")

    resp.plan = plan
    print(resp.model_dump_json())
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """Asks the LLM for a file's content, then saves it with write_file."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    time.sleep(15)
    existing_files = ""
    for s in steps[:coder_state.current_step_idx]:
        existing_files += f"\n--- {s.filepath} ---\n{read_file.run(s.filepath)}\n"

    all_files = ", ".join(s.filepath for s in steps)
    prompt = (
        "You are the CODER agent. Write the complete content of ONE file.\n\n"
        f"Project plan: {coder_state.task_plan.plan}\n"
        f"All files in the project: {all_files}\n"
        f"File to write now: {current_task.filepath}\n"
        f"Task: {current_task.task_description}\n\n"
        f"Files already written (match their ids, classes and data attributes exactly):\n{existing_files}\n\n"
        "Rules:\n"
        "- Output ONLY the raw file content. No explanations, no markdown fences.\n"
        "- Keep it concise (under 80 lines) but fully working.\n"
        "- Use the exact file names listed above when linking files together.\n"
    )

    resp = llm.invoke(prompt)
    code = resp.content.strip()

    # Remove markdown fences if the model added them anyway
    if code.startswith("```"):
        lines = code.split("\n")[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        code = "\n".join(lines)

    write_file.run({"path": current_task.filepath, "content": code})

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}

graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")
agent = graph.compile()