const STORAGE_KEY = "todoList";

let todos = [];

const input = document.getElementById("todo-input");
const addBtn = document.getElementById("add-button");
const list = document.getElementById("todo-list");

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

function load() {
  const data = localStorage.getItem(STORAGE_KEY);
  todos = data ? JSON.parse(data) : [];
}

function render() {
  list.innerHTML = "";
  todos.forEach(t => {
    const li = document.createElement("li");
    li.dataset.id = t.id;
    if (t.completed) li.classList.add("completed");
    li.innerHTML = `<span class="todo-text">${t.text}</span><button class="delete-btn">✖</button>`;
    list.appendChild(li);
  });
}

function addTodo() {
  const text = input.value.trim();
  if (!text) return;
  todos.push({ id: Date.now().toString(), text, completed: false });
  input.value = "";
  save();
  render();
}

function toggleTodo(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
    save();
    render();
  }
}

function deleteTodo(id) {
  todos = todos.filter(t => t.id !== id);
  save();
  render();
}

addBtn.addEventListener("click", addTodo);
input.addEventListener("keydown", e => e.key === "Enter" && addTodo());

list.addEventListener("click", e => {
  const li = e.target.closest("li");
  if (!li) return;
  const id = li.dataset.id;
  if (e.target.matches(".delete-btn")) deleteTodo(id);
  else if (e.target.matches(".todo-text") || e.target === li) toggleTodo(id);
});

document.addEventListener("DOMContentLoaded", () => {
  load();
  render();
});