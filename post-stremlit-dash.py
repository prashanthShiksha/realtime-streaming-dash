import streamlit as st
import psycopg2
import time

# Replace placeholders with your database credentials
conn_string = "postgresql://root:root@localhost:5432/postgres"

# Function to fetch the latest big number from the database
@st.cache_data(ttl=10)
def fetch_latest_number():
    with psycopg2.connect(conn_string) as conn:
        cur = conn.cursor()
        cur.execute("SELECT sum(studentcount) FROM schoolsData")
        result = cur.fetchone()
        return result[0] if result[0] is not None else 0

# Streamlit app
def main():
    st.title("Real-time Big Number")

    placeholder = st.empty()

    while True:
        big_number = fetch_latest_number()

        with placeholder.container():
            st.markdown(f"<h1 style='color: #0066cc;'>{big_number}</h1>", unsafe_allow_html=True)

        time.sleep(1)  # Wait for 1 second before updating

if __name__ == "__main__":
    main()
