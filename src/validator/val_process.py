import messages.messages as messages
import validator.val_token as val_token
import validator.val_session as val_session

def run(operation_data: dict):
    operation_name = 'model_process'
    
    if 'token' not in operation_data:
        return False, messages.MISSING_FIELDS.replace('{operation}', operation_name)
    is_valid, err_msg = val_token.run(operation_data['token'], operation_name)
    if not is_valid:
        return False, err_msg
        
    session_id = operation_data.get('session_id')
    is_valid, err_msg = val_session.run(session_id, operation_name)
    if not is_valid:
        return False, err_msg
        
    if 'input' not in operation_data:
        return False, messages.MISSING_FIELDS.replace('{operation}', operation_name)
    if not isinstance(operation_data['input'], list):
        err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
        return False, err.replace('{details}', "'input' must be an array")
        
    return True, None