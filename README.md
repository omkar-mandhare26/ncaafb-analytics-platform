# **Sports Analytics on NCAAFB Data Using Real-Time API Feeds**

## **Objective**

Build a NCAA Football analytics platform that collects data from the Sportradar NCAAFB API, cleans and stores it in a relational SQL database, and provides an interactive Streamlit dashboard to explore teams, players, seasons, rankings, venues, and coaches, etc. The goal is to create a structured, query-ready dataset for sports analysis and trend insights with search and filter functionalities.

---

# **How to Run This Project**

## **1. Clone the Repository**

```bash
git clone https://github.com/omkar-mandhare26/ncaafb-analytics-platform
cd ncaafb-analytics-platform
```

---

## **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **3. Create Environment File**

Copy the example file:

```bash
cp .env.example .env
```

Update with your API key and DB credentials:

```
API_KEY="your_api_key"
DB_HOST="your_db_host"
DB_PORT="your_db_port"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_NAME="your_db_name"
```

---

## **4. Create Database Tables**

Open and run the notebook:

* `create_table.ipynb`
  This sets up all required SQL tables.

---

## **5. Fetch & Sync Data from API**

Run:

* `sync_api_to_db.ipynb`
  This downloads, cleans, and inserts data into the database.

---

## **6. Start the Streamlit App**

```bash
streamlit run app.py
```

This launches the NCAA Football analytics dashboard.