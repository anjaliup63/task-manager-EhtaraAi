from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import date
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # PROJECTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY,
        name TEXT,
        created_by TEXT
    )
    """)

    # TASKS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        title TEXT,
        status TEXT,
        deadline TEXT,
        project_id INTEGER
    )
    """)

    # SAFE COLUMN ADD
    try:
        cur.execute("ALTER TABLE tasks ADD COLUMN assigned_to TEXT")
    except:
        pass

    # 🔥 DEFAULT ADMIN USER
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users(username,password,role) VALUES ('admin','123','admin')")

    conn.commit()
    conn.close()

# IMPORTANT
init_db()

# ---------------- LOGIN ----------------

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username").strip()
        p = request.form.get("password").strip()

        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
            user = cur.fetchone()

        if user:
            session["user"] = u
            session["role"] = user["role"]
            return redirect("/dashboard")
        else:
            return "Invalid Login ❌"

    return render_template("login.html")

# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        u = request.form.get("username").strip()
        p = request.form.get("password").strip()
        r = request.form.get("role")

        if not u or not p or not r:
            return redirect("/signup")

        with get_db() as conn:
            cur = conn.cursor()

            # prevent duplicate users
            cur.execute("SELECT * FROM users WHERE username=?", (u,))
            if cur.fetchone():
                return "User already exists ❌"

            cur.execute("INSERT INTO users(username,password,role) VALUES (?,?,?)",(u,p,r))

        return redirect("/")

    return render_template("signup.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    with get_db() as conn:
        cur = conn.cursor()

        # ADD TASK
        if request.method == "POST":
            title = request.form.get("title")
            deadline = request.form.get("deadline")
            project_id = request.form.get("project")
            assigned_to = request.form.get("assigned_to")

            if title and deadline and project_id and assigned_to:
                cur.execute("""
                INSERT INTO tasks(title,status,deadline,project_id,assigned_to)
                VALUES (?,?,?,?,?)
                """, (title,"Pending",deadline,project_id,assigned_to))

        # FETCH DATA
        cur.execute("SELECT username FROM users")
        users = cur.fetchall()

        cur.execute("SELECT * FROM projects")
        projects = cur.fetchall()

        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()

    today = str(date.today())

    return render_template(
        "dashboard.html",
        tasks=tasks,
        projects=projects,
        users=users,
        today=today
    )

# ---------------- CREATE PROJECT ----------------

@app.route("/create_project", methods=["POST"])
def create_project():
    if "user" not in session:
        return redirect("/")

    name = request.form.get("name")

    if name:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO projects(name,created_by) VALUES (?,?)",(name,session["user"]))

    return redirect("/dashboard")

# ---------------- COMPLETE TASK ----------------

@app.route("/complete/<int:id>")
def complete(id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET status='Completed' WHERE id=?", (id,))
    return redirect("/dashboard")

# ---------------- DELETE TASK ----------------

@app.route("/delete/<int:id>")
def delete(id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    return redirect("/dashboard")

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- API ROUTES ----------------

@app.route("/api/tasks")
def api_tasks():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        data = [dict(row) for row in cur.fetchall()]
    return jsonify(data)

@app.route("/api/projects")
def api_projects():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects")
        data = [dict(row) for row in cur.fetchall()]
    return jsonify(data)

@app.route("/api/users")
def api_users():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, role FROM users")
        data = [dict(row) for row in cur.fetchall()]
    return jsonify(data)

# ---------------- RUN ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)