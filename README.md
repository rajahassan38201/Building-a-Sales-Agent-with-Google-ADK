# 📞 Sales Agent Project - Using Google ADK LlmAgent + Streamlit

## Features

- True Google ADK `LlmAgent` usage
- Sequential step-by-step conversation
- Dynamic greeting with Lead Name
- CSV storage for leads
- Follow-up reminder simulation

# 🧠 Sales Agent using Google ADK + Streamlit

## Overview

This project implements an intelligent **Sales Agent** powered by the **Google Agent Development Kit (ADK)** and a **Streamlit** web frontend.  
The agent interacts with users, collects lead information step-by-step, and stores the data securely — simulating a real-world sales agent workflow.

## What is Google ADK?

**Google Agent Development Kit (ADK)** is a toolkit designed for building AI-powered conversational agents.  
It simplifies building structured, goal-oriented agents that can maintain memory, handle multi-turn conversations, and take actions based on user input.  
More about it here: [Google ADK GitHub Repository](https://github.com/deepmind/agent-development-kit)

## Project Highlights

- 🎯 Built using **Python**, **Google ADK**, and **Streamlit**.
- 💬 Step-by-step conversational flow to collect user (lead) details.
- 🗂 Data storage in CSV format for leads.
- ⚡ Lightweight, fast, and easy to deploy.

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/your-repository.git
cd sales_agent
```

2. **Set up a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install project dependencies**

```bash
pip install -r requirements.txt
```

4. **Install Google ADK manually**  
   (As it may not be on PyPI yet)

```bash
pip install git+https://github.com/deepmind/agent-development-kit.git
```

## Running the Project

1. **Start the Streamlit application**

```bash
streamlit run app.py
```

2. **Open your browser** and navigate to `http://localhost:8501`  
   The sales agent interface will be ready to use!

## Project Structure

```
sales_agent/
 ├── app.py          # Streamlit frontend
 ├── agents/         # ADK agents and lead handling logic
 ├── leads.csv       # Stored lead data
 ├── requirements.txt
 └── README.md
```

## Requirements

- Python 3.9+
- Streamlit
- Google ADK
- Other Python libraries (in requirements.txt)


---

# 🚀 Get started today and build smarter sales agents with Google ADK!

---

---
