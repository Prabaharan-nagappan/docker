echo "# docker" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Prabaharan-nagappan/docker.git
git push -u origin main

or 

git remote add origin https://github.com/Prabaharan-nagappan/docker.git
git branch -M main
git push -u origin main


Complete example of a Dockerized FastAPI application that performs CRUD (Create, Read, Update, Delete) operations for a simple "Task" entity. This example uses an in-memory data storage, so the data won't persist between container restarts. You can replace it with a database if needed.

1. Install Docker:

   If you haven't already installed Docker on your Ubuntu machine, follow the steps mentioned in the previous response to install Docker.

2. Create a FastAPI Application:

   Create a FastAPI application that performs CRUD operations. Create a Python script, e.g., `app.py`:

   ```python
   # app.py
   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   from typing import List, Optional

   app = FastAPI()

   class Task(BaseModel):
       title: str
       description: Optional[str]

   tasks = []

   @app.post("/tasks/", response_model=Task)
   def create_task(task: Task):
       tasks.append(task)
       return task

   @app.get("/tasks/", response_model=List[Task])
   def read_tasks():
       return tasks

   @app.get("/tasks/{task_id}", response_model=Task)
   def read_task(task_id: int):
       if task_id < 0 or task_id >= len(tasks):
           raise HTTPException(status_code=404, detail="Task not found")
       return tasks[task_id]

   @app.put("/tasks/{task_id}", response_model=Task)
   def update_task(task_id: int, task: Task):
       if task_id < 0 or task_id >= len(tasks):
           raise HTTPException(status_code=404, detail="Task not found")
       tasks[task_id] = task
       return task

   @app.delete("/tasks/{task_id}", response_model=Task)
   def delete_task(task_id: int):
       if task_id < 0 or task_id >= len(tasks):
           raise HTTPException(status_code=404, detail="Task not found")
       deleted_task = tasks.pop(task_id)
       return deleted_task
   ```

3. Create a Dockerfile:

   Create a Dockerfile in the same directory as your FastAPI application with the following content (the same as in the previous responses):

   ```Dockerfile
   # Use the official Python image as a parent image
   FROM python:3.9

   # Set the working directory in the container
   WORKDIR /app

   # Copy the requirements file into the container
   COPY requirements.txt .

   # Install FastAPI and Uvicorn
   RUN pip install fastapi uvicorn

   # Copy your FastAPI application code into the container
   COPY app.py .

   # Expose port 8000 for the FastAPI application
   EXPOSE 8000

   # Command to run the FastAPI application using Uvicorn
   CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

4. Create a requirements.txt file:

   Create a `requirements.txt` file (as previously described) to list the FastAPI and Uvicorn dependencies:

   ```
   fastapi
   uvicorn
   ```

5. Build the Docker Image:

   In your terminal, navigate to the directory containing the Dockerfile and your FastAPI application, and run the following command to build the Docker image:

   ```bash
   docker build -t fastapi-crud-app .
   ```

6. Run the Docker Container:

   Run a Docker container from the built image, mapping port 8000:

   ```bash
   docker run -p 8000:8000 fastapi-crud-app
   ```

7. Access the CRUD API:

   You can now access the CRUD API by opening a web browser or using `curl` to interact with the following endpoints:

   - Create a Task (POST): http://localhost:8000/tasks/
   - Read all Tasks (GET): http://localhost:8000/tasks/
   - Read a specific Task (GET): http://localhost:8000/tasks/{task_id}
   - Update a Task (PUT): http://localhost:8000/tasks/{task_id}
   - Delete a Task (DELETE): http://localhost:8000/tasks/{task_id}

You can use tools like `curl` or Postman to interact with the API, or you can build a front-end application to consume these API endpoints.

Please note that this is a simplified example, and in a real-world scenario, you would typically use a database to store and retrieve data.