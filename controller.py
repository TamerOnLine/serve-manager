import subprocess
import os
import sqlite3
import psutil
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "projects.db")


def get_projects():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, path, entry, port FROM projects")
    projects = cursor.fetchall()
    conn.close()
    return projects


def is_port_in_use(port):
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
            return True
    return False


def start_project(project_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT type, path, entry, port FROM projects WHERE id=?", (project_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return False, "❌ Project not found."

    type_, path, entry, port = result
    full_path = os.path.join(path, entry)

    if not os.path.exists(full_path):
        return False, f"❌ Entry file not found: {full_path}"

    try:
        os.chdir(path)
        if type_ == "flask" or type_ == "python":
            subprocess.Popen(["python", entry])
        elif type_ == "node":
            subprocess.Popen(["node", entry])
        elif type_ == "custom":
            subprocess.Popen(entry, shell=True)
        elif type_ == "html-server":
            os.chdir(entry)  # entry = folder path
            subprocess.Popen(["python", "-m", "http.server", str(port)])
        else:
            return False, f"❌ Unsupported project type: {type_}"
    except Exception as e:
        return False, f"❌ Failed to start: {e}"

    return True, "✅ Project started successfully."


def stop_project(project_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT port FROM projects WHERE id=?", (project_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return False

    port = result[0]

    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if any(str(port) in str(arg) for arg in proc.info["cmdline"]):
                proc.terminate()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return False




def restart_project(project_id):
    if stop_project(project_id):
        time.sleep(1)  # ⏱️ ننتظر ثانية للتأكد من الإغلاق
        return start_project(project_id)
    return False, "❌ Failed to stop the project for restart."


def add_project(name, type_, path, entry, port):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM projects WHERE name = ?", (name,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False, "❌ Project with this name already exists."

    cursor.execute("""
        INSERT INTO projects (name, type, path, entry, port)
        VALUES (?, ?, ?, ?, ?)
    """, (name, type_, path, entry, port))
    conn.commit()
    conn.close()
    return True, "✅ Project added successfully."


def delete_project(project_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    conn.close()
    return True, "🗑️ Project deleted successfully."

def update_project(project_id, name, type_, path, entry, port):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projects
        SET name=?, type=?, path=?, entry=?, port=?
        WHERE id=?
    """, (name, type_, path, entry, port, project_id))
    conn.commit()
    conn.close()
    return True, "✅ Project updated successfully."
