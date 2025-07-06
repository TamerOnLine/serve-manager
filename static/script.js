async function loadProjects() {
  const res = await fetch("/projects");
  const projects = await res.json();
  const list = document.getElementById("project-list");

  list.innerHTML = ""; // مسح الموجود لتجنب التكرار

  projects.forEach(project => {
    const div = document.createElement("div");
    div.style.marginBottom = "10px";

    div.innerHTML = `
      <strong>${project.name}</strong> (${project.type}) - Port: ${project.port}
      <button onclick="startProject(${project.id})">▶️ Start</button>
      <a href="http://localhost:${project.port}" target="_blank">🌐 Open</a>
    `;
    list.appendChild(div);
  });
}

async function startProject(id) {
  await fetch(`/start/${id}`, { method: "POST" });
  alert("✔️ Project started!");
  loadProjects(); // إعادة تحميل الحالة
}

loadProjects();
