#  Team Task Manager (Full-Stack Project)

A simple and efficient full-stack web application to manage projects and tasks with role-based access (Admin / Member).

---

##  Features

*  **Authentication**

  * Signup & Login system
  * Role-based users (Admin / Member)

*  **Project Management**

  * Admin can create projects

*  **Task Management**

  * Create tasks
  * Assign tasks to users
  * Mark tasks as completed
  * Delete tasks

*  **Dashboard**

  * View all tasks
  * Task status (Pending / Completed)
  * Assigned user tracking

*  **REST APIs**

  * `/api/tasks`
  * `/api/projects`
  * `/api/users`

---

##  Tech Stack

* **Frontend:** HTML, CSS
* **Backend:** Python (Flask)
* **Database:** SQLite
* **Deployment:** Railway

---

##  How to Run Locally

```bash
git clone https://github.com/your-username/task-manager.git
cd task-manager
pip install -r requirements.txt
python app.py
```

👉 Open in browser:
https://task-manager-ehtaraai-production.up.railway.app/

---

##  Default Login

```
Username: admin  
Password: 123
```

---

##  API Endpoints

* Get all tasks → `/api/tasks`
* Get all projects → `/api/projects`
* Get all users → `/api/users`

---

##  Project Structure

```
task-manager/
│── app.py
│── requirements.txt
│── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
```

---

##  Note

* Currently using SQLite (local database)
* For production, can be upgraded to PostgreSQL for persistent storage

---

##  Highlights

* Full-stack implementation
* Role-based access control
* Clean UI with modern design
* REST API integration

---

##  Author

**Anjali Upadhyay**
