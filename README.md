# Process-Scheduling-Simulator-Using-Frontend-and-Backend
Project Overview
This is a web-based Process Scheduling Simulator that demonstrates key CPU scheduling algorithms: First Come First Serve (FCFS), Shortest Job First (SJF), and Round Robin (RR). The project consists of a frontend built with HTML, CSS, and JavaScript for user interaction and visualization, and a backend powered by Python Flask that processes scheduling logic and returns results.

Features
Input dynamic number of processes with Arrival Time and Burst Time

Select scheduling algorithm (FCFS, SJF, RR)

Round Robin supports user-defined quantum time

Displays detailed process table with Completion Time, Waiting Time, and Turnaround Time

Visual Gantt chart showing the scheduling timeline

Seamless communication between frontend and backend via Flask API

Project Structure
php
Copy
Edit
process-scheduling-simulator/
│
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── static/                # Frontend static files (CSS, JS)
│   ├── style.css
│   └── script.js
└── templates/
    └── index.html         # Frontend HTML template
How to Run
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the Flask server:

bash
Copy
Edit
python app.py
Open your browser and go to:
http://127.0.0.1:5000



Technologies Used
Python 3.x, Flask

HTML5, CSS3

JavaScript (Vanilla JS)
