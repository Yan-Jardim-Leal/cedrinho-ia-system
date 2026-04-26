import messages.messages as messages
import data_manager
import uuid
import validator
import os

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
         return messages.INTERNAL_ERROR.replace('{operation}', 'model_create').replace('{details}', 'Falha ao compilar o modelo matematico')

    db_success = data_manager.storeData(operation_data)
    if not db_success:
        return messages.INTERNAL_ERROR.replace('{operation}', 'model_create').replace('{details}', 'Falha de I/O no banco de dados SQLite')

    return messages.MODEL_CREATED.replace('{token}', token)

def compile_and_save_ai(data_payload: dict) -> bool:
    """
    Função stub. Irá ler o array 'layers', construir a rede e salvar o arquivo .h5.
    """
    print(f"[S] Compilando modelo para {data_payload['file_path']}...")
    try:
        with open(data_payload['file_path'], 'w') as f:
            f.write("BINARY_DUMMY_DATA")
        return True
    except Exception:
        return False