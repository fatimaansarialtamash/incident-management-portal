import sqlite3


def create_database():

    conn = sqlite3.connect("incidents.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        priority TEXT,
        status TEXT,
        assigned_to TEXT,
        created_date TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_incident(
        incident_id,
        title,
        description,
        priority,
        status,
        assigned_to,
        created_date
):

    conn = sqlite3.connect("incidents.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO incidents
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        incident_id,
        title,
        description,
        priority,
        status,
        assigned_to,
        created_date
    ))

    conn.commit()
    conn.close()


def get_all_incidents():

    conn = sqlite3.connect("incidents.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM incidents"
    )

    incidents = cursor.fetchall()

    conn.close()

    return incidents


def search_incident(incident_id):

    conn = sqlite3.connect("incidents.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM incidents WHERE incident_id = ?",
        (incident_id,)
    )

    incident = cursor.fetchone()

    conn.close()

    return incident


def get_incident_counts():

    conn = sqlite3.connect("incidents.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM incidents"
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM incidents WHERE status='Open'"
    )
    open_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM incidents WHERE status='In Progress'"
    )
    progress_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM incidents WHERE status='Closed'"
    )
    closed_count = cursor.fetchone()[0]

    conn.close()

    return (
        total,
        open_count,
        progress_count,
        closed_count
    )


def generate_incident_id():

    conn = sqlite3.connect("incidents.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM incidents"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return f"INC{count + 1:03d}"


def update_incident_status(
        incident_id,
        status
):

    conn = sqlite3.connect("incidents.db")

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE incidents
    SET status = ?
    WHERE incident_id = ?
    """, (
        status,
        incident_id
    ))

    conn.commit()
    conn.close()


def get_incidents_by_priority(priority):

    conn = sqlite3.connect("incidents.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM incidents WHERE priority = ?",
        (priority,)
    )

    incidents = cursor.fetchall()

    conn.close()

    return incidents


create_database()