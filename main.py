from agent.tools import set_project_name
from agent.graph import agent


def main():
    name = input("Project folder name (e.g. todo-app): ")
    user_prompt = input("What app do you want to build? ")

    root = set_project_name(name)
    print("Output folder:", root)

    result = agent.invoke(
        {"user_prompt": user_prompt},
        {"recursion_limit": 100},
    )
    print("Final State:", result)


if __name__ == "__main__":
    main()