import json
import os.path
import sqlite3
import aiofiles


class Export:
    class_table = '''
    CREATE TABLE IF NOT EXISTS class_models (
        id INTEGER PRIMARY KEY,
        code_model_id INTEGER,
        class_name TEXT,
        modifiers TEXT,
        properties TEXT,
        start_lin_no INTEGER,
        start_pos INTEGER,
        end_lin_no INTEGER,
        end_pos INTEGER,
        FOREIGN KEY (code_model_id) REFERENCES code_models(id)
    )
    '''

    method_table = '''
    CREATE TABLE IF NOT EXISTS method_models (
        id INTEGER PRIMARY KEY,
        class_model_id INTEGER,
        method_name TEXT,
        modifiers TEXT,
        body TEXT,
        start_lin_no INTEGER,
        start_pos INTEGER,
        end_lin_no INTEGER,
        end_pos INTEGER,
        FOREIGN KEY (class_model_id) REFERENCES class_models(id)
    )
    '''

    commit_table = '''
    CREATE TABLE IF NOT EXISTS commit_models (
        id INTEGER PRIMARY KEY,
        code_model_id INTEGER,
        commit_id TEXT,
        author TEXT,
        email TEXT,
        message TEXT,
        date TEXT,
        FOREIGN KEY (code_model_id) REFERENCES code_models(id)
    )
    '''

    file_table = '''
    CREATE TABLE IF NOT EXISTS code_models (
        id INTEGER PRIMARY KEY,
        language TEXT,
        filepath TEXT,
        namespace TEXT,
        imports TEXT
    )
    '''

    def __init__(self, project):
        self.project = project

    async def run_export_async(self):
        export_data = self.project.data

        # Path to the SQLite database
        os.makedirs(self.project.project_output_dir, exist_ok=True)
        db_path = os.path.join(self.project.project_output_dir, "data.db")

        # Connect to SQLite database (it will create it if it doesn't exist)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(self.file_table)
        cursor.execute(self.class_table)
        cursor.execute(self.method_table)
        cursor.execute(self.commit_table)

        # Insert data into the database
        for key in export_data.keys():
            code_model = export_data[key]

            cursor.execute("INSERT INTO code_models (language, filepath, namespace, imports) VALUES (?, ?, ?, ?)",
                           (code_model.language, key, code_model.namespace, json.dumps(code_model.imports)))
            code_model_id = cursor.lastrowid

            for class_model in code_model.code_classes:
                cursor.execute("INSERT INTO class_models (code_model_id, class_name, modifiers, properties, start_lin_no, start_pos, end_lin_no, end_pos) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (code_model_id, class_model.name, json.dumps(class_model.modifiers), json.dumps(class_model.properties),
                                class_model.start_lin_no, class_model.start_pos, class_model.end_lin_no, class_model.end_pos))
                class_model_id = cursor.lastrowid

                for method in class_model.methods:
                    cursor.execute("INSERT INTO method_models (class_model_id, method_name, modifiers, body, "
                                   "start_lin_no, start_pos, end_lin_no, end_pos) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                   (class_model_id, method.name, json.dumps(method.modifiers), method.body,
                                    method.start_lin_no, method.start_pos, method.end_lin_no, method.end_pos))

            for commit in code_model.commits:
                cursor.execute(
                    "INSERT INTO commit_models (code_model_id, commit_id, author, email, message, date) VALUES (?, ?, ?, ?, ?, ?)",
                    (code_model_id, commit.commit_hash, commit.commit_author, commit.commit_author_email,commit.commit_message, commit.commit_date))


        # Commit the transaction and close the connection
        connection.commit()
        connection.close()

        print(f"Data has been exported to {db_path}")

