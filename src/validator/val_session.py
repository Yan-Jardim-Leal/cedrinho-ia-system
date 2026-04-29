import messages.messages as messages

MIN_SESSION_LENGTH = 20

def run(session_id, operation_name):
    if session_id is not None:
        if not isinstance(session_id, str):
            err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
            return False, err.replace('{details}', 'session_id must be a string')
            
        if len(session_id) < MIN_SESSION_LENGTH:
            err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
            return False, err.replace('{details}', f'Invalid session_id format, should be at least {MIN_SESSION_LENGTH} characters long')
            
    return True, None