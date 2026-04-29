import messages.messages as messages
import validator.val_token as val_token

def run(operation_data: dict):
    operation_name = 'model_load'
    
    if 'token' not in operation_data:
        return False, messages.MISSING_FIELDS.replace('{operation}', operation_name)
        
    is_valid, err_msg = val_token.run(operation_data['token'], operation_name)
    if not is_valid:
        return False, err_msg
        
    return True, None