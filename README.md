Instructions
  To run the dashboard, use the following command in the terminal:
  streamlit run app.py
  
  To update the database with new data:
  Place your telemetry file in the data/ directory and name it:
  telemetry_logs.jsonl
  Place your employee file in the data/ directory and name it:
  employees.csv
  
  Run the ingestion script:
  python -m scripts.ingest_data
  
  This will parse the data, validate it, and update the SQLite database.

Architecture
  The project is structured into several components:

  1. Data Ingestion Layer
    Parses raw telemetry logs (jsonl)
    Loads employee data (csv)
    Cleans and validates data
    Stores processed data into SQLite database

  Main files:
    utils/parse_telemetry.py
    utils/load_employees.py
    scripts/ingest_data.py

  2. Database Layer
    SQLite database (analytics.db)
    Stores structured data in tables:
      api_requests
      employees
      Prevents duplicate entries using unique event IDs
       
    Main file:
      utils/database.py

  3. Data Access Layer
    Loads and joins data from the database
    Applies transformations (date, hour, etc.)
    Provides data to the dashboard

    Main file:
      utils/load_from_db.py

  4. Dashboard Layer
    Built using Streamlit
    Multi-page interface:
      Home (overview & key insights)
      Overview (KPIs & trends)
      Analysis (detailed breakdowns)
      Insights (advanced analytics)
     
    Includes:
      Interactive filters (sidebar)
      Charts and tables for analysis

    Main files:
      app.py
      pages/

      
Dependencies
  The project uses the following libraries:
    Streamlit — for building the interactive dashboard
    Pandas — for data processing and analysis
    SQLite3 — for storing structured data in a database
    Plotly — for creating interactive charts

LLM Usage Log
  ChatGPT (OpenAI) — used for:
    understanding telemetry data structure
    designing the data pipeline
    generating initial code templates
    improving dashboard structure and insights

  Example Promtps:
    1. Data Parsing & Pipeline Design<br>
      "How should I parse nested JSONL telemetry logs and extract only relevant fields for analysis?"<br>
    👉 Result:<br>
      Implemented a parser for api_request events<br>
      Designed a clean data extraction pipeline<br>
    2. Database Design<br>
      "What is the best schema for storing telemetry usage data for a dashboard?"<br>
    👉 Result:<br>
      Created normalized tables (api_requests, employees)<br>
      Used event IDs as primary keys to prevent duplicates<br>
    3. Dashboard Design<br>
      "What insights should a usage analytics dashboard show?"<br>
    👉 Result:<br>
      Added KPIs (tokens, cost, users, sessions)<br>
      Implemented charts for usage trends, model usage, and performance<br>
      Added anomaly detection and top-user analysis<br>
    4. Data Validation<br>
      "How should I validate and clean telemetry data before storing it?"<br>
    👉 Result:<br>
      Implemented filtering for missing/invalid values<br>
      Added type conversions and constraints (e.g., non-negative tokens)<br>

  All AI-generated code and suggestions were manually reviewed and validated.
