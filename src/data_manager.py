import sqlite3
import json
import messages.messages as messages

DATABASE_NAME = 'data.db'

def run():
    """Inicializa a base de dados. Deve ser chamado no startServer()."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT UNIQUE NOT NULL,
                file_path TEXT NOT NULL,
                learning_type TEXT,
                
                architecture TEXT,
                training_config TEXT,
                rl_params TEXT,

                status TEXT DEFAULT 'idle',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_token ON data (token);
        ''')
        conn.commit()
    print("[D] Banco de dados estruturado e verificado.")

def storeData(data_payload: dict):
    """Armazena os metadados do modelo e serializa blocos complexos de JSON."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            token = data_payload.get('token')
            file_path = data_payload.get('file_path')
            learning_type = data_payload.get('learning_type')
            
            architecture = json.dumps(data_payload.get('architecture', {}))
            training_config = json.dumps(data_payload.get('training_config', {}))
            rl_params = json.dumps(data_payload.get('rl_params', {}))

            cursor.execute('''
                INSERT INTO data (
                    token, file_path, learning_type, 
                    architecture, training_config, rl_params
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (token, file_path, learning_type, architecture, training_config, rl_params))
            
            conn.commit()
            return True
            
    except Exception as e:
        print(f"[ERROR] data_manager.storeData: {e}")
        return False

def retrieveData(token: str):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM data WHERE token = ?', (token,))
            row = cursor.fetchone()
            return row
    except Exception as e:
        print(f"[ERROR] data_manager.retrieveData: {e}")
        return None

def deleteData(token: str):
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM data WHERE token = ?', (token,))
            conn.commit()
            return True
    except Exception as e:
        print(f"[ERROR] data_manager.deleteData: {e}")
        return False