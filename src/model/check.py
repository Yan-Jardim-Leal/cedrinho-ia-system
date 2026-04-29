import data_manager

def run(operation_data: dict, active_models: dict) -> dict:
    token = operation_data['token']
    
    model_entry = data_manager.retrieveData(token)
    if not model_entry:
        return {
            "message": "Token not found in the database.",
            "error": True,
            "training_remaining": None,
            "loaded": None,
            "last_trained": None
        }

    status = model_entry[7]
    last_trained = model_entry[8]
    is_loaded = token in active_models

    return {
        "message": f"Model current status: {status}",
        "error": False,
        "training_remaining": 0, # Placeholder para fila de treino futura
        "loaded": is_loaded,
        "last_trained": str(last_trained)
    }