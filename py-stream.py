import faust
import psycopg2

app = faust.App('kafka_to_postgres', broker='kafka://localhost:9092')

# Define a topic and keep the value_type to the default (no need to specify str)
topic = app.topic('realtime.dashboard')

# PostgreSQL connection details
DB_PARAMS = {
    "dbname": "postgres",
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}

# Function to connect to PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        return conn, cursor
    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None, None

@app.agent(topic)
async def process_messages(stream):
    conn, cursor = get_db_connection()
    if not conn or not cursor:
        print("Failed to connect to PostgreSQL. Exiting agent.")
        return

    async for data in stream:
        try:
            # Now data is expected to be a dictionary
            school_name = data["schoolName"]
            student_count = data["studentCount"]

            # Insert data into PostgreSQL
            sql = "INSERT INTO schoolsData (schoolName, studentCount) VALUES (%s, %s)"
            cursor.execute(sql, (school_name, student_count))
            conn.commit()

        except Exception as e:
            print(f"Error processing message: {e}")
            conn.close()
            conn, cursor = get_db_connection()

if __name__ == '__main__':
    app.main()
