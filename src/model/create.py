import messages.messages as messages
import data_manager
import uuid
import validator
import os

import tensorflow as tf 
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL
STORAGE_DIR = "../storage/models"

def run(operation_data: dict):
    is_valid, error_msg = validator.validate_model_create(operation_data)
    if not is_valid:
        return messages.VALIDATION_ERROR.replace('{operation}', 'model_create').replace('{details}', error_msg)

    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    token = str(uuid.uuid4())
    file_path = os.path.join(STORAGE_DIR, f"{token}.h5")

    operation_data['token'] = token
    operation_data['file_path'] = file_path

    compilation_success = compile_and_save_ai(operation_data)
    if not compilation_success:
         return messages.INTERNAL_ERROR.replace('{operation}', 'model_create').replace('{details}', 'Failed to compile and save the mathematical model')

    db_success = data_manager.storeData(operation_data)
    if not db_success:
        return messages.INTERNAL_ERROR.replace('{operation}', 'model_create').replace('{details}', 'Failed I/O operation on SQLite database')

    return messages.MODEL_CREATED.replace('{token}', token)

def compile_and_save_ai(data_payload: dict) -> bool:
    """
    Constrói a rede neural baseada na arquitetura validada e salva em formato .h5.
    """
    print(f"[S] Compilando modelo para {data_payload['file_path']}...")
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