import sqlite3
import json
from models import Snakes, Owners, Species


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
            s.color, 
            o.first_name owner_first, 
            o.last_name owner_last, 
            o.email owner_email, 
            sp.name species_name
        FROM Snakes s
        JOIN Owners o 
            ON o.id = s.owner_id
        JOIN Species sp 
            ON sp.id = s.species_id
        """)

        snakes = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snakes(row['id'], row['name'], row['owner_id'],
                           row['species_id'], row['gender'], row['color'])
            owner = Owners(row['owner_id'], row['owner_first'],
                           row['owner_last'], row['owner_email'])

            species = Species(row['species_id'], row['species_name'])

            del snake.owner_id
            del snake.species_id

            snake.owner = owner.__dict__
            snake.species = species.__dict__

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
            s.color, 
            o.first_name owner_first, 
            o.last_name owner_last, 
            o.email owner_email, 
            sp.name species_name
        FROM Snakes s
        JOIN Owners o 
            ON o.id = s.owner_id
        JOIN Species sp 
            ON sp.id = s.species_id
        WHERE s.id = ?
        """, (id, ))

        data = db_cursor.fetchone()
        # Create an order instance from the current row
        snake = Snakes(data['id'], data['name'], data['owner_id'],
                       data['species_id'], data['gender'], data['color'])

        owner = Owners(data['owner_id'], data['owner_first'],
                       data['owner_last'], data['owner_email'])

        species = Species(data['species_id'], data['species_name'])

        del snake.owner_id
        del snake.species_id

        snake.owner = owner.__dict__
        snake.species = species.__dict__

        return snake.__dict__


def get_snake_by_species(gender):
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
        WHERE s.gender = ?
        """, (gender, ))

        snakes = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snakes(row['id'], row['name'], row['owner_id'],
                           row['species_id'], row['gender'], row['color'])
            snakes.append(snake.__dict__)

    return snakes


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
