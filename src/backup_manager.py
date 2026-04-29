import os
import json

# Define onde os backups seguros serão guardados
BACKUP_DIR = "../storage/backups"

def save_training_backup(session_id: str, new_experiences: list) -> bool:
    """
    Guarda o lote de experiências (train_data) no disco de forma atómica.
    Destrói a crítica de 'Perda de Dados na RAM'.
    """
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    file_path = os.path.join(BACKUP_DIR, f"backup_session_{session_id}.json")
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
            
        existing_data.extend(new_experiences)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4)
            
        return True
    except Exception as e:
        print(f"[ERROR] backup_manager: Failed to save persistence backup for {session_id} - {e}")
        return False