import sqlite3

def display_table():
    # Connect to the database
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()

    # List all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("📂 Tables in the database:")
    for table in tables:
        table_name = table[0]
        print(f"\n🔹 Table: {table_name}")
        
        cursor.execute(f"PRAGMA table_info({table_name})")  # Show table schema
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print("Columns:", column_names)

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("⚠️ No data found in this table.")

    conn.close()
