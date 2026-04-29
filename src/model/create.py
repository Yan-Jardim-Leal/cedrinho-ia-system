import data_manager
import uuid
import os
import tensorflow as tf 
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input

STORAGE_DIR = "../storage/models"

def run(operation_data: dict) -> dict:
    """
    Recebe o payload (já validado pelo FastAPI), processa a criação,
    grava no disco e no SQLite, e retorna um dicionário compatível com ModelCreateResponse.
    """
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    token = str(uuid.uuid4())
    file_path = os.path.join(STORAGE_DIR, f"{token}.keras")

    operation_data['token'] = token
    operation_data['file_path'] = file_path

    compilation_success = compile_and_save_ai(operation_data)
    if not compilation_success:
        return {
            "message": "Failed to compile and save the mathematical model.",
            "error": True
        }

    db_success = data_manager.storeData(operation_data)
    if not db_success:
        return {
            "message": "Failed I/O operation on SQLite database.",
            "error": True
        }

    return {
        "message": "Model created successfully.",
        "token": token,
        "error": False
    }

def compile_and_save_ai(data_payload: dict) -> bool:
    """
    Constrói a rede neural baseada na arquitetura validada e salva em formato .keras.
    """
    print(f"[CEDRI] Compilando modelo para {data_payload['file_path']}...")
    try:
        model = Sequential()
        layers_config = data_payload['architecture']['layers']
        
        for index, layer_data in enumerate(layers_config):
            layer_type = layer_data['type'].lower()
            units = layer_data['units']
            
            if index == 0:
                input_shape = tuple(layer_data['input_shape'])
                model.add(Input(shape=input_shape))
            
            if layer_type == 'dense':
                model.add(Dense(units))
            elif layer_type == 'lstm':
                model.add(LSTM(units))
                
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        model.save(data_payload['file_path'])
        return True
        
    except Exception as e:
        print(f"[ERROR] compile_and_save_ai: {e}")
        return False