# 🏥 Insurance Premium Prediction API

A RESTful API built with **FastAPI** that predicts insurance premium categories based on user health and demographic data. The project demonstrates data validation with **Pydantic**, ML model serving, and containerization with **Docker**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Run Locally](#run-locally)
  - [Run with Docker](#run-with-docker)
- [API Reference](#api-reference)
- [Input & Output Schema](#input--output-schema)
- [Feature Engineering](#feature-engineering)
- [Environment & Configuration](#environment--configuration)

---

## Overview

This API accepts basic user information (age, weight, height, city, occupation, income, smoking status) and returns a predicted **insurance premium tier** (e.g., Low, Medium, High) along with confidence scores and class probabilities.

The model is a pre-trained scikit-learn classifier loaded at startup. Pydantic handles all input validation and automatically computes derived features like BMI, lifestyle risk, age group, and city tier — so the model always receives clean, consistent input.

---

## Project Structure

```
.
├── app.py                  # FastAPI application and route definitions
├── Dockerfile              # Container image definition
├── requirements.txt        # Python dependencies
├── model/
│   ├── model.pkl           # Pre-trained scikit-learn classifier
│   └── predict.py          # Model loading and prediction logic
└── schema/
    ├── client_input.py     # Pydantic input model with validation & computed fields
    └── response.py         # Pydantic response model
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Data Validation | [Pydantic v2](https://docs.pydantic.dev/) |
| ML / Inference | [scikit-learn](https://scikit-learn.org/), [pandas](https://pandas.pydata.org/) |
| Server | [Uvicorn](https://www.uvicorn.org/) |
| Containerization | [Docker](https://www.docker.com/) |

---

## Features

- **Input validation** — strict type checks, range enforcement, and allowed-value constraints via Pydantic
- **Automatic feature engineering** — BMI, lifestyle risk score, age group, and city tier are computed from raw inputs before hitting the model
- **Health check endpoint** — exposes model version and load status
- **Interactive docs** — auto-generated Swagger UI at `/docs` and ReDoc at `/redoc`
- **Dockerized** — single command to build and run anywhere

---

## Getting Started

### Prerequisites

- Python 3.11+ (for local run)
- Docker (for containerized run)

### Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

### Run with Docker

```bash
# 1. Build the image
docker build -t insurance-prediction-api .

# 2. Run the container
docker run -p 8000:8000 insurance-prediction-api
```

The API will be available at `http://localhost:8000`.

---

## API Reference

### `GET /`

Welcome message and usage hint.

**Response**
```json
{
  "message": "Welcome to the Insurance Premium Prediction API. Use the /predict endpoint to get a premium prediction based on your data."
}
```

---

### `GET /health`

Check API and model status.

**Response**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "model_loaded": true
}
```

---

### `POST /predict`

Predict insurance premium tier.

**Request body**
```json
{
  "age": 35,
  "weight": 75.0,
  "height": 1.75,
  "income_lpa": 12.5,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

**Response**
```json
{
  "Response": {
    "predicted_class": "Medium",
    "Confidence": 0.7823,
    "class_probabilities": {
      "Low": 0.15,
      "Medium": 0.7823,
      "High": 0.0677
    }
  }
}
```

---

## Input & Output Schema

### Input Fields (`POST /predict`)

| Field | Type | Constraints | Description |
|---|---|---|---|
| `age` | `int` | 0 – 120 | Age in years |
| `weight` | `float` | > 0 | Weight in kilograms |
| `height` | `float` | > 0 | Height in meters |
| `income_lpa` | `float` | > 0 | Annual income in lakhs (LPA) |
| `smoker` | `bool` | `true` / `false` | Smoking status |
| `city` | `str` | Any city name | Normalized to title case automatically |
| `occupation` | `str` | See below | Must be one of the allowed values |

**Allowed `occupation` values:**
`retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job`

### Response Fields

| Field | Type | Description |
|---|---|---|
| `predicted_class` | `str` | Predicted premium tier (e.g., `Low`, `Medium`, `High`) |
| `Confidence` | `float` | Probability of the predicted class (0–1) |
| `class_probabilities` | `dict` | Probability for each possible class |

---

## Feature Engineering

Raw user inputs are never sent directly to the model. Pydantic `@computed_field` properties automatically derive the following features:

| Computed Feature | Logic |
|---|---|
| `bmi` | `weight / height²` |
| `lifestyle_risk` | `high` if smoker + BMI > 30; `medium` if smoker or BMI > 27; else `low` |
| `age_group` | `young` (< 25), `adult` (< 45), `middle-aged` (< 60), `senior` (60+) |
| `city_tier` | `1` for metro cities, `2` for Tier-2 cities, `3` for all others |

These computed features — not the raw inputs — are what the model uses for prediction.

---

## Environment & Configuration

No environment variables are required to run the app. The model is loaded from `model/model.pkl` at startup.

To verify the model loaded correctly after startup, call `GET /health` and confirm `"model_loaded": true`.

---

## Interactive Documentation

Once the server is running, visit:

- **Swagger UI** → `http://localhost:8000/docs`
- **ReDoc** → `http://localhost:8000/redoc`
