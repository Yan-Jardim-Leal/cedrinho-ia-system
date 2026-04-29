import numpy as np
import backup_manager

def run(operation_data: dict, active_models: dict, active_sessions: dict) -> dict:
    token = operation_data['token']
    session_id = operation_data['session_id']
    train_data = operation_data['train_data']

    if token not in active_models:
        return {
            "message": "Model is not loaded in RAM. Call model_load first.",
            "error": True,
            "session_id": session_id
        }

    if session_id not in active_sessions:
        active_sessions[session_id] = {"history": [], "state": None}

    try:
        model = active_models[token]
        
        x_train = np.array([step['state'] for step in train_data])
        y_train = np.array([step['action'] for step in train_data]) 
        
        epochs = operation_data.get('epochs', 1)
        model.fit(x_train, y_train, epochs=epochs, verbose=0)
        
        backup_manager.save_training_backup(session_id, train_data)

        return {
            "message": f"Successfully processed and trained on {len(train_data)} experience steps. Backup created.",
            "error": False,
            "session_id": session_id
        }
    except Exception as e:
        print(f"[ERROR] train.run: {e}")
        return {
            "message": f"Internal training error: {str(e)}",
            "error": True,
            "session_id": session_id
        }