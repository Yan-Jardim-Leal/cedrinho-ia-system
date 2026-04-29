import numpy as np

def run(operation_data: dict, active_models: dict, active_sessions: dict) -> dict:
    token = operation_data['token']
    session_id = operation_data['session_id']
    input_data = operation_data['input']

    if token not in active_models:
        return {
            "message": "Model is not loaded in RAM. Call model_load first.",
            "error": True,
            "output": None,
            "session_id": session_id
        }

    if session_id not in active_sessions:
        active_sessions[session_id] = {"history": [], "state": None}

    try:
        model = active_models[token]
        prediction = model.predict(np.array([input_data]), verbose=0)
        
        active_sessions[session_id]["history"].append(input_data)
        
        return {
            "message": "Model processed successfully.",
            "error": False,
            "output": prediction.tolist()[0],
            "session_id": session_id
        }
    except Exception as e:
        print(f"[ERROR] process.run: {e}")
        return {
            "message": f"Failed to process inference: {str(e)}",
            "error": True,
            "output": None,
            "session_id": session_id
        }