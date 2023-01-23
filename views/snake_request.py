import sqlite3
import json
from models import Snakes


def get_all_snakes():
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.name, 
            s.owner_id, 
            s.species_id, 
            s.gender, 
            s.color
        FROM Snakes s
        """)

        snakes = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snakes(row['id'], row['name'], row['owner_id'],
                           row['species_id'], row['gender'], row['color'])

            snakes.append(snake.__dict__)
    return snakes


def get_single_snakes(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.name, 
            s.owner_id, 
            s.species_id, 
            s.gender, 
            s.color
        FROM Snakes s
        WHERE s.id = ? 
        """, (id, ))

        data = db_cursor.fetchone()
        # Create an order instance from the current row
        snake = Snakes(data['id'], data['name'], data['owner_id'],
                       data['species_id'], data['gender'], data['color'])

        return snake.__dict__


def create_snake(new_snake):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Snakes
            (name, owner_id, species_id, gender, color)
        VALUES
            (?, ?, ?, ?, ?); 
        """, (new_snake['name'], new_snake['owner_id'], new_snake['species_id'], new_snake['gender'], new_snake['color']))

        id = db_cursor.lastrowid
        new_snake['id'] = id
    return new_snake
