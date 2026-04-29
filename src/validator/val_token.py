import messages.messages as messages

MIN_TOKEN_LENGTH = 20

def run(token, operation_name):
    if not token:
        return False, messages.MISSING_FIELDS.replace('{operation}', operation_name)
    
    if not isinstance(token, str):
        err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
        return False, err.replace('{details}', 'Token must be a string')
        
    if len(token) < MIN_TOKEN_LENGTH:
        err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
        return False, err.replace('{details}', f'Invalid token format, should be at least {MIN_TOKEN_LENGTH} characters long')
        
    return True, None