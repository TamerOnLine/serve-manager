import subprocess
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "projects.db")

def get_projects():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, path, entry, port FROM projects")
    projects = cursor.fetchall()
    conn.close()
    return projects

def start_project(project_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT type, path, entry FROM projects WHERE id=?", (project_id,))
    project = cursor.fetchone()
    conn.close()

    if not project:
        return False

    type_, path, entry = project
    os.chdir(path)

    if type_ == "flask":
        subprocess.Popen(["python", entry])
    elif type_ == "node":
        subprocess.Popen(["node", entry])
    else:
        return False

    return True
