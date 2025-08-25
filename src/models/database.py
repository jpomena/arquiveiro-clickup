import sqlite3 as sql
import pathlib
import os


class Database:
    def __init__(self):
        home_dir = pathlib.Path.home()

        if os.name == 'nt':
            db_path = os.getenv('LOCALAPPDATA')
            db_dir = pathlib.Path(db_path) / 'ArquiveiroClickUp'
        else:
            db_dir = home_dir / 'ArquiveiroClickUp'

        db_dir.mkdir(parents=True, exist_ok=True)
        self._db_file = db_dir / 'tasks.db'

    def _connect(self):
        conn = sql.connect(self._db_file)
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn

    def create_table(self):
        create_tasks_table_sql = '''
            CREATE TABLE IF NOT EXISTS tasks(
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                task_tag TEXT NOT NULL,
                task_assignee TEXT NOT NULL,
                task_backlog_date TEXT NOT NULL,
                task_start_date TEXT NOT NULL,
                task_done_date TEXT NOT NULL,
                task_delivery_date TEXT NOT NULL
            );'''

        conn = self._connect()

        try:
            cursor = conn.cursor()
            cursor.execute(create_tasks_table_sql)
            conn.commit()
        finally:
            conn.close()

    def save_task_data(self, task_data):
        insert_task_data_sql = '''
            INSERT INTO tasks(
                task_name,
                task_tag,
                task_assignee,
                task_backlog_date,
                task_start_date,
                task_done_date,
                task_delivery_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        conn = self._connect()

        try:
            cursor = conn.cursor()
            if task_data['done_date'] == 'N/A':
                task_data['done_date'] = task_data['delivery_date']
            task_values = (
                task_data.get('task_name', 'N/A'),
                task_data.get('task_tag', 'N/A'),
                task_data.get('task_assignee', 'N/A'),
                task_data.get('backlog_date', 'N/A'),
                task_data.get('start_date', 'N/A'),
                task_data.get('done_date', 'N/A'),
                task_data.get('delivery_date', 'N/A')
            )

            cursor.execute(insert_task_data_sql, task_values)
            conn.commit()
        finally:
            conn.close()

    def get_db_tasks_data(self):
        get_task_data_sql = '''
            SELECT
                task_name,
                task_tag,
                task_assignee,
                task_backlog_date,
                task_start_date,
                task_done_date,
                task_delivery_date
            FROM tasks
        '''

        conn = self._connect()
        db_task_data = []

        try:
            cursor = conn.cursor()
            cursor.execute(get_task_data_sql)
            query_results = cursor.fetchall()

            for result in query_results:
                task = {
                    'task_name': result[0],
                    'task_tag': result[1],
                    'task_assignee': result[2],
                    'task_backlog_date': result[3],
                    'task_start_date': result[4],
                    'task_done_date': result[5],
                    'task_delivery_date': result[6]
                }
                db_task_data.append(task)
        finally:
            conn.close()

        return db_task_data
