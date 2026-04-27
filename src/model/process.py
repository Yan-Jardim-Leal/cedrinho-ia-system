import numpy as np
import uuid
import messages.messages as messages

def run(operation_data, active_models, active_sessions):
    token = operation_data.get('token')
    session_id = operation_data.get('session_id')
    input_data = operation_data.get('input')

    if token not in active_models:
        return messages.RAM_ERROR.replace('{operation}', 'model_process')

    if not session_id or session_id not in active_sessions:
        session_id = str(uuid.uuid4())
        active_sessions[session_id] = {"history": [], "state": None}

    try:
        model = active_models[token]
        prediction = model.predict(np.array(input_data))
        
        active_sessions[session_id]["history"].append(input_data)
        
        res = messages.MODEL_PROCESSED.replace('{output}', str(prediction.tolist()))
        return res.replace('}', f', "session_id": "{session_id}"' + '}')
    except Exception as e:
        return messages.INTERNAL_ERROR.replace('{operation}', 'model_process').replace('{details}', str(e))