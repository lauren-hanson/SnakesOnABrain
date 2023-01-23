import sqlite3
import json
from models import Snakes, Species, Owners


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
            sp.id species_id,
            sp.name species_name, 
            o.first_name owner_first, 
            o.last_name owner_last, 
            o.email owner_email
        FROM Snakes s
        JOIN Species sp 
            ON sp.id = s.species_id
        JOIN Owners o 
            ON o.id = s.owner_id
        """)

        snakes = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snakes(row['id'], row['name'], row['owner_id'],
                           row['species_id'], row['gender'], row['color'])

            species = Species(row['species_id'], row['species_name'])

            owner = Owners(row['owner_id'], row['owner_first'],
                           row['owner_last'], row['owner_email'])

            snake.species = species.__dict__
            snake.owner = owner.__dict__

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
            sp.id species_id,
            sp.name species_name, 
            o.first_name owner_first, 
            o.last_name owner_last, 
            o.email owner_email
        FROM Snakes s
        JOIN Species sp 
            ON sp.id = s.species_id
        JOIN Owners o 
            ON o.id = s.owner_id
        WHERE s.id = ? 
        """, (id, ))

        data = db_cursor.fetchone()
        # Create an order instance from the current row
        snake = Snakes(data['id'], data['name'], data['owner_id'],
                       data['species_id'], data['gender'], data['color'])
        species = Species(data['species_id'], data['species_name'])
        owner = Owners(data['owner_id'], data['owner_first'],
                       data['owner_last'], data['owner_email'])

        snake.species = species.__dict__
        snake.owner = owner.__dict__

        return snake.__dict__


def get_snake_by_species(species):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.name, 
            s.owner_id, 
            s.species_id, 
            s.gender, 
            s.color
        FROM Snakes s
        WHERE s.species_id = ? 
        """, (species, ))

        snakes = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snakes(row['id'], row['name'], row['owner_id'],
                           row['species_id'], row['gender'], row['color'])

            snakes.append(snake.__dict__)
    return snakes
