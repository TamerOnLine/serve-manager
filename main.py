from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controller import restart_project, add_project


from pydantic import BaseModel


import os

from controller import get_projects, start_project, stop_project, is_port_in_use

# 🗂️ مسارات الملفات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# 🚀 إعداد FastAPI
app = FastAPI()

# 🧩 تحميل الملفات الثابتة والقوالب
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# 🏠 الصفحة الرئيسية
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 📄 API: عرض جميع المشاريع مع الحالة
@app.get("/projects")
def list_projects():
    projects = get_projects()
    return [
        {
            "id": p[0],
            "name": p[1],
            "type": p[2],
            "port": p[5],
            "status": "🟢 Running" if is_port_in_use(p[5]) else "🔴 Stopped"
        }
        for p in projects
    ]


# ▶️ API: تشغيل مشروع
@app.post("/start/{project_id}")
def start(project_id: int):
    success, message = start_project(project_id)
    return {"status": "ok" if success else "error", "message": message}


# ⏹️ API: إيقاف مشروع
@app.post("/stop/{project_id}")
def stop(project_id: int):
    success = stop_project(project_id)
    return {"status": "ok" if success else "error", "message": "🛑 Stopped" if success else "❌ Not Found or Already Stopped"}




@app.post("/restart/{project_id}")
def restart(project_id: int):
    success, message = restart_project(project_id)
    return {"status": "ok" if success else "error", "message": message}




class ProjectData(BaseModel):
    name: str
    type: str
    path: str
    entry: str
    port: int

@app.post("/add")
def add(data: ProjectData):
    success, message = add_project(
        data.name, data.type, data.path, data.entry, data.port
    )
    return {"status": "ok" if success else "error", "message": message}

from controller import delete_project

@app.post("/delete/{project_id}")
def delete(project_id: int):
    success, message = delete_project(project_id)
    return {"status": "ok" if success else "error", "message": message}


@app.put("/update/{project_id}")
def update(project_id: int, data: ProjectData):
    success, message = update_project(
        project_id, data.name, data.type, data.path, data.entry, data.port
    )
    return {"status": "ok" if success else "error", "message": message}
