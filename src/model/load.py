import tensorflow as tf
import data_manager
import messages.messages as messages

def run(operation_data, active_models):
    token = operation_data.get('token')
    if not token:
        return messages.MISSING_FIELDS.replace('{operation}', 'model_load')

    model_entry = data_manager.retrieveData(token)
    if not model_entry:
        return messages.INTERNAL_ERROR.replace('{operation}', 'model_load').replace('{details}', 'Token not found')

    file_path = model_entry[2]

    try:
        print(f"[S] Carregando modelo {token} para a RAM...")
        model = tf.keras.models.load_model(file_path, compile=False)
        active_models[token] = model
        return messages.MODEL_LOADED
    except Exception as e:
        return messages.INTERNAL_ERROR.replace('{operation}', 'model_load').replace('{details}', str(e))