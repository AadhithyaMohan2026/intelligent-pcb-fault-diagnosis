# Intelligent PCB Fault Diagnosis & Maintenance Platform

A full-stack application that analyzes electrical measurements from printed circuit boards (PCBs) to identify potential faults and provide diagnostic insights and maintenance recommendations.

## Overview

Troubleshooting PCB faults manually can be time-consuming and requires careful analysis of electrical parameters. This project combines machine learning and rule-based diagnosis to help identify common PCB fault conditions from measured inputs.

The application provides a web interface for entering measurements, a backend API for processing diagnostic requests, and a PostgreSQL database for storing diagnosis records.

## Key Features

- **PCB Fault Classification:** Identifies potential fault categories from electrical measurements.
- **Hybrid Diagnosis:** Combines machine learning predictions with rule-based diagnostic logic.
- **Confidence and Severity:** Presents prediction confidence and fault severity information.
- **Diagnostic Insights:** Provides suspected fault areas, supporting evidence, and troubleshooting recommendations.
- **Web Interface:** Allows users to enter PCB measurements and view diagnostic results.
- **Database Integration:** Stores diagnostic records for future reference and analysis.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, JavaScript, Vite |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Machine Learning | Python, scikit-learn |
| Data Format | CSV, JSON |
| API | REST API, HTTP |

## Input Parameters

The system analyzes eight electrical and thermal parameters:

- Supply voltage
- Input current
- Regulator output voltage
- Microcontroller voltage
- Temperature
- Ripple voltage
- Signal frequency
- Continuity

## Fault Categories

The dataset and diagnostic system cover the following classes:

- Normal
- Short Circuit
- Open Circuit
- Regulator Failure
- Overheating
- Sensor Failure

## System Architecture

1. **Measurement Input:** The user enters PCB measurement values through the React interface.
2. **API Processing:** The FastAPI backend validates and processes the submitted measurements.
3. **Fault Prediction:** The machine learning model and rule-based logic analyze the input.
4. **Diagnostic Output:** The application returns the predicted condition, confidence, severity, and recommendations.
5. **Record Storage:** PostgreSQL stores the diagnostic results for later reference.

## Dataset

The project includes a PCB measurement dataset in CSV format.

- Dataset location: `data/raw/pcb_measurements.csv`
- Number of records: 6,000
- Input features: 8
- Target classes: 6

The dataset was divided into 4,800 training records and 1,200 testing records.

**Reported model accuracy:** 99.5% on the test set.

This result applies to the project's test dataset and should not be interpreted as a guarantee of performance on real-world PCB measurements.

## Project Structure

```text
pcb-diagnostic-platform/
├── backend/
├── frontend/
├── data/
│   ├── raw/
│   │   └── pcb_measurements.csv
│   └── processed/
├── database/
├── .gitignore
└── README.md
```

The folders shown above represent the intended organization. Refer to the actual repository files for the implemented modules and scripts.

## Running the Project Locally

### Prerequisites

- Python
- Node.js and npm
- PostgreSQL

### 1. Backend Setup

From the project root, activate your Python virtual environment and install the dependencies listed in your backend requirements file.

Start the backend with:

```bash
uvicorn backend.main:app --reload
```

The API should be available at:

`http://127.0.0.1:8000`

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

### 2. Frontend Setup

Open a terminal in the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in your terminal, usually:

`http://localhost:5173`

### 3. Database Configuration

Ensure PostgreSQL is running and the project database is configured correctly. Set the required connection details using environment variables or the configuration method used by the backend.

Do not commit database passwords, secret keys, or private environment files to the repository.

## Future Improvements

- Validate the model against real-world PCB fault measurements.
- Add diagnostic history, filtering, and visualization.
- Improve fault localization and explainability.
- Add automated testing and model performance monitoring.
- Explore deployment and role-based access control.

## Project Status

Developed as an electronics and software engineering project combining PCB diagnostics, machine learning, backend API development, frontend development, and relational database integration.
