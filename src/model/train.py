import numpy as np
import uuid
import messages.messages as messages

def run(operation_data, active_models, active_sessions):
    token = operation_data.get('token')
    session_id = operation_data.get('session_id')
    x_train = np.array(operation_data.get('x'))
    y_train = np.array(operation_data.get('y'))
    epochs = operation_data.get('epochs', 1)

    if token not in active_models:
        return messages.RAM_ERROR.replace('{operation}', 'model_train')

    if not session_id or session_id not in active_sessions:
        session_id = str(uuid.uuid4())
        active_sessions[session_id] = {"history": [], "state": None}

    try:
        model = active_models[token]
        history = model.fit(x_train, y_train, epochs=epochs, verbose=0)
        
        return messages.MODEL_TRAINED.replace('{session_id}', session_id)
    except Exception as e:
        return messages.INTERNAL_ERROR.replace('{operation}', 'model_train').replace('{details}', str(e))