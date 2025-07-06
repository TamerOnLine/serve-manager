from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from controller import get_projects, start_project

# 📦 مسارات ديناميكية بالكامل
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# 🚀 إعداد FastAPI
app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# 🏠 صفحة التحكم
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 📄 API: قائمة المشاريع
@app.get("/projects")
def list_projects():
    projects = get_projects()
    return [
        {"id": p[0], "name": p[1], "type": p[2], "port": p[5]}
        for p in projects
    ]

# ▶️ API: تشغيل مشروع
@app.post("/start/{project_id}")
def start(project_id: int):
    success = start_project(project_id)
    return {"status": "ok" if success else "error"}
