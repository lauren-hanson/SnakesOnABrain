import sqlite3
import json
from models import Species


def get_all_species():
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            sp.id,
            sp.name
        FROM Species sp
        """)

        species = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            specie = Species(row['id'], row['name'])

            species.append(specie.__dict__)
    return species


def get_single_species(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            sp.id,
            sp.name
        FROM Species sp
        WHERE sp.id = ? 
        """, (id, ))

        data = db_cursor.fetchone()
        # Create an order instance from the current row
        specie = Species(data['id'], data['name'])

        return specie.__dict__
