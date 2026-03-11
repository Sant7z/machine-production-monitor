# Machine Production Monitor

Industrial production monitoring system developed in Python.

This project simulates a real-world industrial monitoring solution used to validate production data, detect anomalies in machine processes, store records in a database, expose data through an API, and visualize information in a dashboard.

## Features

- Load production data from CSV
- Validate mass values and detect anomalies
- Store production records in SQLite
- Generate execution logs
- Expose production data through FastAPI
- Visualize machine status in a Streamlit dashboard

## Technologies

- Python
- Pandas
- SQLite
- FastAPI
- Streamlit

## Project Structure

```text
machine-production-monitor/
├── data/
│   └── production_data.csv
├── database/
│   └── production.db
├── logs/
│   └── system.log
├── src/
│   ├── api.py
│   ├── dashboard.py
│   ├── data_reader.py
│   ├── database.py
│   ├── logger.py
│   ├── main.py
│   └── validator.py
├── .gitignore
├── README.md
└── requirements.txt