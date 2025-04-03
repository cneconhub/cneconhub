import sqlite3 as sq
from typing import Literal, TypeVar
from importlib import resources
from pathlib import Path
from . import __res__


def get_databses() -> list[str]:
	"""Get a list of string containing all databases
	"""
	datasets: list[str] = []
	for file in resources.files(__res__).iterdir():
		filepath = Path(str(file))
		if filepath.suffix == '.db':
			datasets.append(filepath.name)
	return datasets

def get_database_tables(database: str) -> list[str]:
	"""Get a list of string containing all tables of the database

	Input:
		- database (str): name of a database suffixed by `.db`
	"""
	table_names: list[str] = []
	with resources.path(__res__, database) as file:
		db = sq.connect(file)
		cursor = db.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables: list[tuple[str]] = cursor.fetchall()
		table_names = [tab[0] for tab in tables]
		cursor.close()
		db.close()
	return table_names

def get_database_tableinfo(database: str, table: str) -> list[tuple]:
	"""Get the information of a table in a database

	Input:
		- database (str): name of a database suffixed by `.db`
		- table (str): name of a table in database
	"""
	columns: list[tuple] = []
	with resources.path(__res__, database) as file:
		db = sq.connect(file)
		cursor = db.cursor()
		cursor.execute(f"PRAGMA table_info({table});")
		columns = cursor.fetchall()
		cursor.close()
		db.close()
	return columns
