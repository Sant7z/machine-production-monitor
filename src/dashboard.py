import streamlit as st
import sqlite3
import pandas as pd

MIN_MASS = 95
MAX_MASS = 105


def get_connection():
    return sqlite3.connect("database/production.db")


def load_data_from_db():
    conn = get_connection()
    query = "SELECT machine_id, mass, timestamp FROM production_data"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", errors="coerce")

    return df


def insert_uploaded_data(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO production_data (machine_id, mass, timestamp)
            VALUES (?, ?, ?)
            """,
            (row["machine_id"], float(row["mass"]), str(row["timestamp"]))
        )

    conn.commit()
    conn.close()


def get_machine_status(df):
    latest = df.sort_values("timestamp").groupby("machine_id").tail(1).copy()
    latest["status"] = latest["mass"].apply(
        lambda m: "ALERT" if m < MIN_MASS or m > MAX_MASS else "OK"
    )
    return latest.sort_values("machine_id")


def get_alerts(df):
    return df[(df["mass"] < MIN_MASS) | (df["mass"] > MAX_MASS)]


st.set_page_config(page_title="Machine Monitor", layout="wide")

st.title("🏭 Machine Production Monitor")
st.caption("Industrial production monitoring and anomaly detection")

st.sidebar.header("Data Source")

uploaded_file = st.sidebar.file_uploader(
    "Upload a production CSV file",
    type=["csv"]
)

use_database = st.sidebar.checkbox("Use database data", value=True)

df = pd.DataFrame()

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", errors="coerce")

    st.sidebar.success("CSV loaded successfully")

    if st.sidebar.button("Save uploaded data to database"):
        insert_uploaded_data(df)
        st.sidebar.success("Data saved to database")

elif use_database:
    df = load_data_from_db()

if df.empty:
    st.warning("No data available. Upload a CSV file or populate the database first.")
    st.stop()

status_df = get_machine_status(df)
alerts_df = get_alerts(df)

col1, col2, col3 = st.columns(3)
col1.metric("Total records", len(df))
col2.metric("Alerts detected", len(alerts_df))
col3.metric("Machines monitored", df["machine_id"].nunique())

st.divider()
st.subheader("Machine Status")

for _, row in status_df.iterrows():
    if row["status"] == "OK":
        st.success(f"{row['machine_id']} — OK (mass={row['mass']})")
    else:
        st.error(f"{row['machine_id']} — ALERT (mass={row['mass']})")

st.divider()

machine_list = sorted(df["machine_id"].unique())
selected_machine = st.selectbox(
    "Select machine to view history",
    ["All"] + machine_list
)

if selected_machine != "All":
    filtered_df = df[df["machine_id"] == selected_machine].copy()
else:
    filtered_df = df.copy()

st.subheader("Mass Trend")
chart_df = filtered_df.sort_values("timestamp").set_index("timestamp")
st.line_chart(chart_df["mass"])

st.subheader("Production Data")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("Detected Anomalies")
filtered_alerts = get_alerts(filtered_df)
inserted = insert_uploaded_data(df)
st.sidebar.success(f"{inserted} new records inserted")
if not filtered_alerts.empty:
    st.dataframe(filtered_alerts, use_container_width=True)
else:
    st.success("No anomalies detected.")