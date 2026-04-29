def run(operation_data: dict, active_models: dict) -> dict:
    token = operation_data['token']
    
    if token in active_models:
        model = active_models.pop(token)
        del model
        
        return {
            "message": "Model unloaded successfully.", 
            "error": False
        }
        
    return {
        "message": "Model was not in RAM.", 
        "error": False
    }