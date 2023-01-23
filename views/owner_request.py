import sqlite3
import json
from models import Owners


def get_all_owners():
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id, 
            o.first_name, 
            o.last_name, 
            o.email
        FROM Owners o
        """)

        owners = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            owner = Owners(row['id'], row['first_name'], row['last_name'], row['email'])

            owners.append(owner.__dict__)
    return owners


def get_single_owners(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id, 
            o.first_name, 
            o.last_name, 
            o.email
        FROM Owners o
        WHERE o.id = ? 
        """, (id, ))

        data = db_cursor.fetchone()
        # Create an order instance from the current row
        owner = Owners(data['id'], data['first_name'], data['last_name'], data['email'])

        return owner.__dict__
