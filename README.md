# Mini Workflow Engine — Tredence AI Engineering Internship Assignment

A lightweight, extensible agent workflow engine built using **FastAPI**, showcasing Python backend design, async execution, state management, conditional branching, looping logic, and live run inspection.

This project demonstrates the core backend engineering skills required for the Tredence AI Engineering Internship — including API design, workflow orchestration, structured state handling, and clean code architecture.

---

##  What This Project Does

This engine allows you to:

- Define **nodes** (steps) that execute Python functions  
- Maintain a shared **state dictionary** flowing through the workflow  
- Define **edges** to control transitions between nodes  
- Perform **conditional branching** using safe rule evaluation  
- Support **loops** with `max_iterations`  
- Register and call **custom tools**  
- Run workflows **asynchronously**  
- Track progress via:
  - `GET /graph/state/{run_id}` — live state  
  - `POST /graph/wait/{run_id}` — block until completion  
- Cancel running workflows using:
  - `POST /graph/cancel/{run_id}`  

---

## Tech Stack

- **Python 3.11+**
- **FastAPI**
- **Uvicorn**
- **AsyncIO**
- **Pydantic**

---

## Project Structure

trendance/
│── app/
│   ├── main.py               # FastAPI routes and initialization
│   ├── models.py             # Pydantic models for logs & requests
│   │
│   ├── engine/
│       ├── graph.py          # Core workflow engine
│       ├── tools.py          # Tool registry and sample tools
│       ├── workflows.py      # Predefined sample workflows
│       ├── safe_eval.py      # Secure condition evaluator
│
│── requirements.txt
│── README.md
│── .gitignore

## How to Run Locally

### **1. Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate 
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```
### **3. Start FastAPI server**
```bash
uvicorn app.main:app --reload --port 8000
```
### **3. Open Swagger API UI**
- **[link](http://127.0.0.1:8000/docs)**

## Core API Endpoints

### **1. Create a Graph**
- **POST /graph/create**
  - **Defines nodes + edges**

---

### **2. Run a Graph**
- **POST /graph/run**

  **Example Request**
  ```json
  {
    "graph_id": "code_review_sample",
    "initial_state": {
      "code": "def a(): pass",
      "threshold": 70
    }
  }
**Example Response**
```json
{
  "run_id": "6100cf19-8cbe-4045-92cd-baab4e6b94e4"
}
```
### **3. Get Live State**
-**GET /graph/state/{run_id}**
  -**Shows**:
    -**current node**
    -**workflow status**
    -**entire state**
    -**execution logs**
    
### **4. Wait Until Completion**
-**POST /graph/wait/{run_id}**
  -**Blocks until workflow finishes**

### **5. Cancel Workflow**
-**POST /graph/cancel/{run_id}**
  -** Response**
  ```json
  {
  "status": "cancelled"
}
```

## Safe Condition Evaluator

We avoid Python's unsafe `eval()` and use a restricted evaluator allowing:

- Boolean logic  
- Arithmetic  
- Comparisons  
- State access (`state["quality_score"]`)

**Disallowed:** function calls, attribute access, imports, or any arbitrary code execution.


<img width="1681" height="943" alt="Screenshot 2025-12-10 at 10 41 51 PM" src="https://github.com/user-attachments/assets/945aad37-5615-40ab-82a7-2aae08e8a0d9" />



## Author

**Anuchand C**    
Tredence 2025  
[LinkedIn]([https://www.linkedin.com/](https://www.linkedin.com/in/anuchand-chelladurai/)) 







