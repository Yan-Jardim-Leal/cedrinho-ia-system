import tensorflow as tf
import data_manager

def run(operation_data: dict, active_models: dict) -> dict:
    token = operation_data['token']

    model_entry = data_manager.retrieveData(token)
    if not model_entry:
        return {
            "message": "Token not found in the database.",
            "error": True
        }

    # O file_path é o 3º elemento (índice 2) no db
    file_path = model_entry[2]

    try:
        print(f"[CEDRI] Carregando modelo {token} para a RAM...")
        model = tf.keras.models.load_model(file_path, compile=False)
        active_models[token] = model
        
        return {
            "message": "Model loaded into RAM successfully.",
            "error": False
        }
    except Exception as e:
        print(f"[ERROR] load.run: {e}")
        return {
            "message": f"Failed to load the model file: {str(e)}",
            "error": True
        }