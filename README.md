# 🐳 Docker Cloud Notes App

A containerized web application built with **Flask, PostgreSQL, Docker, and Docker Compose**.

This project demonstrates how to take a web application, package it into a Docker image, run it as a container, connect it to a PostgreSQL database container, and persist database data using Docker volumes.

---

## 📌 Project Overview

The **Docker Cloud Notes App** is a simple notes application where users can:

* Create notes
* View saved notes
* Delete notes
* Check application health

The complete application runs using Docker containers.

### Architecture

```text
                    Browser
                       |
                       | http://localhost:5000
                       ↓
              ┌─────────────────┐
              │   Flask Web     │
              │    Container    │
              │                 │
              │  Python + Flask │
              └────────┬────────┘
                       |
                       | Docker Network
                       |
                       ↓
              ┌─────────────────┐
              │   PostgreSQL    │
              │    Container    │
              │                 │
              │   cloudnotes    │
              └────────┬────────┘
                       |
                       ↓
              ┌─────────────────┐
              │ Docker Volume   │
              │ postgres-data   │
              │                 │
              │ Persistent Data │
              └─────────────────┘
```

---

# 🛠️ Technologies Used

* **Python 3.12**
* **Flask 3.1.2**
* **PostgreSQL 16**
* **Docker**
* **Docker Compose**
* **Docker Volumes**
* **Docker Networks**
* **HTML/CSS**
* **psycopg2**

---

# 📂 Project Structure

```text
docker-project/
│
├── app/
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       └── style.css
│
├── db/
│   └── init.sql
│
├── Dockerfile
├── compose.yaml
├── .dockerignore
└── README.md
```

---

# 🧩 Application Components

## 1. Flask Web Application

The Flask application provides the web interface and API routes.

Main routes:

| Route          | Method | Purpose                  |
| -------------- | ------ | ------------------------ |
| `/`            | GET    | Display all notes        |
| `/add`         | POST   | Add a new note           |
| `/delete/<id>` | POST   | Delete a note            |
| `/health`      | GET    | Check application health |

---

# 🗄️ PostgreSQL Database

PostgreSQL runs inside its own Docker container.

Database configuration:

```text
Database: cloudnotes
User: postgres
Port: 5432
```

The application connects to PostgreSQL using Docker's internal network.

The important setting is:

```text
DATABASE_HOST=postgres
```

`postgres` is the Docker Compose service name.

Docker Compose provides internal DNS, so the Flask container can find the PostgreSQL container using:

```text
postgres
```

Instead of:

```text
localhost
```

---

# 🐳 Dockerfile

The Dockerfile creates the image for the Flask application.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
```

## Dockerfile Explanation

### Base Image

```dockerfile
FROM python:3.12-slim
```

Uses a lightweight Python image.

### Working Directory

```dockerfile
WORKDIR /app
```

Sets `/app` as the working directory inside the container.

### Install Dependencies

```dockerfile
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
```

Dependencies are installed before copying the application source code.

This improves Docker build caching.

### Copy Application

```dockerfile
COPY app/ .
```

Copies the Flask application into the image.

### Non-Root User

```dockerfile
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser
```

The application does not run as root.

This improves container security.

### Expose Application Port

```dockerfile
EXPOSE 5000
```

Documents that Flask listens on port `5000`.

---

# 🐙 Docker Compose

Docker Compose manages both containers.

```yaml
services:

  web:
    build: .
    container_name: cloud-notes-web

    ports:
      - "5000:5000"

    environment:
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_NAME: cloudnotes
      DATABASE_USER: postgres
      DATABASE_PASSWORD: postgres

    depends_on:
      postgres:
        condition: service_healthy

    networks:
      - cloud-notes-network

  postgres:
    image: postgres:16

    container_name: cloud-notes-db

    environment:
      POSTGRES_DB: cloudnotes
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/01-init.sql:ro

    networks:
      - cloud-notes-network

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d cloudnotes"]
      interval: 5s
      timeout: 5s
      retries: 5

networks:
  cloud-notes-network:

volumes:
  postgres-data:
```

---

# 🌐 Docker Networking

Both services use:

```yaml
networks:
  - cloud-notes-network
```

This creates a private Docker network.

The Flask application connects to PostgreSQL using:

```text
postgres:5432
```

The communication looks like:

```text
Flask Container
      |
      | postgres:5432
      ↓
PostgreSQL Container
```

We don't need to expose PostgreSQL's port `5432` to the host because Flask communicates with PostgreSQL internally through the Docker network.

---

# 💾 Docker Volumes

PostgreSQL uses a named Docker volume:

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

The volume stores PostgreSQL's database files outside the container's writable layer.

Therefore:

```text
PostgreSQL Container
       ↓
postgres-data Volume
       ↓
Database Files
```

If the PostgreSQL container is removed and recreated, the data remains because the volume still exists.

---

# 🧪 Testing Persistent Storage

A persistence test was performed by:

1. Adding a note.
2. Checking the note in PostgreSQL.
3. Removing the PostgreSQL container.
4. Keeping the Docker volume.
5. Recreating the PostgreSQL container.
6. Checking the database again.

Example:

```bash
docker compose stop postgres
docker compose rm postgres
docker compose up -d postgres
```

The previously stored notes remain available.

This demonstrates that the Docker volume is working correctly.

> **Important:** Do not use `docker compose down -v` when testing persistence because `-v` removes the volumes.

---

# 🏗️ Build the Project

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Enter the project:

```bash
cd docker-project
```

Build the Docker images:

```bash
docker compose build
```

---

# ▶️ Start the Application

Run:

```bash
docker compose up -d
```

The `-d` option runs the containers in detached mode.

Check the containers:

```bash
docker compose ps
```

Expected result:

```text
cloud-notes-web
cloud-notes-db
```

---

# 🌐 Access the Application

Open your browser:

```text
http://localhost:5000
```

You should see:

```text
🐳 Docker Cloud Notes

Flask + PostgreSQL running with Docker
```

---

# 🏥 Health Check

The application provides:

```text
http://localhost:5000/health
```

Expected response:

```json
{
  "application": "Docker Cloud Notes App",
  "status": "healthy"
}
```

---

# 🗄️ Check the Database

Open a PostgreSQL shell inside the container:

```bash
docker exec -it cloud-notes-db psql -U postgres -d cloudnotes
```

List tables:

```sql
\dt
```

Check notes:

```sql
SELECT * FROM notes;
```

Exit PostgreSQL:

```sql
\q
```

---

# 🔍 Check Docker Logs

Check Flask logs:

```bash
docker compose logs web
```

Follow Flask logs:

```bash
docker compose logs -f web
```

Check PostgreSQL logs:

```bash
docker compose logs postgres
```

Follow PostgreSQL logs:

```bash
docker compose logs -f postgres
```

---

# 📦 Check Docker Images

Run:

```bash
docker images
```

Or:

```bash
docker compose images
```

---

# 💾 Check Docker Volumes

Run:

```bash
docker volume ls
```

Inspect the volume:

```bash
docker volume inspect docker-project_postgres-data
```

The exact volume name may be different depending on the project directory name.

---

# 🌐 Check Docker Networks

Run:

```bash
docker network ls
```

Inspect the project network:

```bash
docker network inspect docker-project_cloud-notes-network
```

The exact network name may differ depending on the project directory name.

---

# 🛑 Stop the Application

To stop the containers:

```bash
docker compose stop
```

This stops the containers but does not remove them.

---

# 🗑️ Remove Containers

To stop and remove the containers:

```bash
docker compose down
```

The PostgreSQL volume remains.

Therefore, database data remains available when the project is started again.

---

# ⚠️ Remove Everything Including Database Data

Only use this when you intentionally want to delete the PostgreSQL data:

```bash
docker compose down -v
```

The `-v` option removes the Docker volumes.

---

# 🔐 Environment Variables

The application uses environment variables for database configuration.

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

The Flask application reads these values using Python:

```python
os.getenv("DATABASE_HOST")
```

This allows the same application image to be configured differently in different environments.

### Production Note

The password used in this learning project is:

```text
postgres
```

For production environments, passwords should not be hardcoded.

A production deployment should use a secure secrets-management solution such as Docker secrets, Kubernetes Secrets, or a cloud secrets service.

---

# 🗃️ Database Initialization

The project contains:

```text
db/init.sql
```

The SQL creates the `notes` table:

```sql
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

The file is mounted into PostgreSQL:

```yaml
- ./db/init.sql:/docker-entrypoint-initdb.d/01-init.sql:ro
```

PostgreSQL automatically executes initialization scripts when the database is initialized for the first time.

---

# 🔄 Application Flow

When a user creates a note:

```text
1. User enters a note
        ↓
2. Browser sends POST request
        ↓
3. Flask receives the request
        ↓
4. Flask connects to PostgreSQL
        ↓
5. PostgreSQL stores the note
        ↓
6. Data is stored in Docker volume
        ↓
7. Flask redirects to homepage
        ↓
8. Note appears on the screen
```

---

# 🧠 Docker Concepts Demonstrated

This project demonstrates the following Docker concepts:

### 1. Docker Images

The Flask application is packaged into a Docker image.

```bash
docker compose build
```

### 2. Docker Containers

The application runs inside a Flask container.

```text
cloud-notes-web
```

PostgreSQL runs inside another container:

```text
cloud-notes-db
```

### 3. Dockerfile

Defines how the Flask image is built.

### 4. Docker Compose

Manages multiple containers together.

### 5. Container Networking

Allows Flask to communicate with PostgreSQL.

### 6. Environment Variables

Used to configure database connection details.

### 7. Docker Volumes

Persist PostgreSQL data.

### 8. Health Checks

Docker checks whether PostgreSQL is ready.

### 9. Container Security

The Flask application runs as a non-root user.

### 10. Docker Build Caching

Dependencies are copied and installed before application source code.

---

# 🔐 Security Improvements

The project includes some basic security practices:

* Flask container runs as a non-root user.
* PostgreSQL is not exposed directly to the host.
* Application and database communicate through a private Docker network.
* Dependencies are explicitly versioned.
* Database data is stored in a persistent volume.
* `.dockerignore` prevents unnecessary files from being included in the Docker build context.

For production, additional improvements would include:

* Secrets management
* HTTPS/TLS
* Production WSGI server such as Gunicorn
* Image vulnerability scanning
* Smaller/optimized images
* Resource limits
* Container health monitoring
* CI/CD pipeline

---

# 🧹 .dockerignore

The project uses `.dockerignore` to prevent unnecessary files from being sent to the Docker build context.

Example:

```text
__pycache__
*.pyc
*.pyo
*.pyd

.venv
venv
env

.git
.gitignore

.env

README.md
```

This helps keep the Docker build context smaller and prevents unnecessary files from being copied into the image.

---

# 🧪 Useful Docker Commands

### List containers

```bash
docker ps
```

### List all containers

```bash
docker ps -a
```

### List images

```bash
docker images
```

### List volumes

```bash
docker volume ls
```

### List networks

```bash
docker network ls
```

### View logs

```bash
docker compose logs
```

### Rebuild

```bash
docker compose build
```

### Start

```bash
docker compose up -d
```

### Stop

```bash
docker compose stop
```

### Remove containers

```bash
docker compose down
```

---

# 📚 Learning Outcomes

After completing this project, I learned how to:

* Understand containers and Docker images
* Create a Dockerfile
* Build Docker images
* Run containers
* Use Docker Compose
* Run multiple services together
* Configure applications using environment variables
* Connect containers using Docker networking
* Run PostgreSQL inside a container
* Use Docker volumes for persistent storage
* Create database initialization scripts
* Configure container health checks
* Run containers as non-root users
* Debug containers using Docker logs
* Inspect Docker networks and volumes
* Verify persistent database storage

---

# 🚀 Future Improvements

Possible future improvements include:

* Add Gunicorn
* Add Nginx as a reverse proxy
* Add Docker image security scanning
* Add GitHub Actions CI/CD
* Add automated testing
* Add Prometheus monitoring
* Add Grafana dashboards
* Add HTTPS
* Move secrets to a secure secrets manager
* Deploy the application to Kubernetes
* Deploy the application to AWS

---

# 👨‍💻 Author

**Aleem Ahmad**

BS Mathematics
Namal University

Interested in:

* DevOps
* Cloud Engineering
* Kubernetes
* Docker
* Terraform
* CI/CD
* AI for DevOps

---

# ⭐ Project Goal

The goal of this project is to demonstrate practical knowledge of **Docker containerization and multi-container application deployment** by building and running a Flask + PostgreSQL application using Docker Compose.

```text
Source Code
     ↓
Dockerfile
     ↓
Docker Image
     ↓
Docker Container
     ↓
Docker Compose
     ↓
Flask + PostgreSQL
     ↓
Persistent Docker Volume
     ↓
Running Application 🚀
```
