let allProjects = [];

async function loadProjects() {
  const res = await fetch("/projects");
  const projects = await res.json();
  allProjects = projects;

  const list = document.getElementById("project-list");
  list.innerHTML = "";

  projects.forEach(project => {
    const div = document.createElement("div");
    div.id = `project-${project.id}`;
    div.style.marginBottom = "10px";

    const status = project.status;
    const restartBtn = `<button onclick="restartProject(${project.id})">🔄 Restart</button>`;
    const deleteBtn = `<button onclick="deleteProject(${project.id})">🗑️ Delete</button>`;
    const editBtn = `<button onclick="editProjectById(${project.id})">✏️ Edit</button>`;

    const controls = status.includes("Running")
      ? `<button onclick="stopProject(${project.id})">⏹️ Stop</button> ${restartBtn} ${deleteBtn} ${editBtn}`
      : `<button onclick="startProject(${project.id})">▶️ Start</button> ${deleteBtn} ${editBtn}`;

    div.innerHTML = `
      <strong>${project.name}</strong> (${project.type}) - Port: ${project.port}
      ${controls}
      <a href="http://localhost:${project.port}" target="_blank">🌐 Open</a>
      <span style="margin-left: 10px;">${status}</span>
    `;

    list.appendChild(div);
  });
}

async function startProject(id) {
  const res = await fetch(`/start/${id}`, { method: "POST" });
  const result = await res.json();
  alert(result.status === "ok" ? "✔️ " + result.message : "❌ Error: " + result.message);
  loadProjects();
}

async function stopProject(id) {
  const res = await fetch(`/stop/${id}`, { method: "POST" });
  const result = await res.json();
  alert(result.status === "ok" ? "🛑 " + result.message : "❌ Error: " + result.message);
  loadProjects();
}

async function restartProject(id) {
  const res = await fetch(`/restart/${id}`, { method: "POST" });
  const result = await res.json();
  alert(result.status === "ok" ? "🔄 " + result.message : "❌ Error: " + result.message);
  loadProjects();
}

async function deleteProject(id) {
  if (!confirm("⚠️ Are you sure you want to delete this project?")) return;
  const res = await fetch(`/delete/${id}`, { method: "POST" });
  const result = await res.json();
  alert(result.message);
  loadProjects();
}

function editProjectById(id) {
  const project = allProjects.find(p => p.id === id);
  editProject(project);
}

function editProject(project) {
  const form = document.createElement("form");
  form.innerHTML = `
    <input type="text" value="${project.name}" id="edit-name-${project.id}">
    <input type="text" value="${project.type}" id="edit-type-${project.id}">
    <input type="text" value="${project.path}" id="edit-path-${project.id}">
    <input type="text" value="${project.entry}" id="edit-entry-${project.id}">
    <input type="number" value="${project.port}" id="edit-port-${project.id}">
    <button onclick="saveProject(event, ${project.id})">💾 Save</button>
  `;

  const div = document.getElementById(`project-${project.id}`);
  div.innerHTML = "";
  div.appendChild(form);
}

async function saveProject(event, id) {
  event.preventDefault();
  const data = {
    name: document.getElementById(`edit-name-${id}`).value,
    type: document.getElementById(`edit-type-${id}`).value,
    path: document.getElementById(`edit-path-${id}`).value,
    entry: document.getElementById(`edit-entry-${id}`).value,
    port: parseInt(document.getElementById(`edit-port-${id}`).value),
  };

  const res = await fetch(`/update/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  alert(result.message);
  loadProjects();
}

async function addProject(event) {
  event.preventDefault();
  const data = {
    name: document.getElementById("name").value,
    type: document.getElementById("type").value,
    path: document.getElementById("path").value,
    entry: document.getElementById("entry").value,
    port: parseInt(document.getElementById("port").value),
  };

  const res = await fetch("/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  alert(result.message);
  loadProjects();
  document.getElementById("add-form").reset();
}

loadProjects();