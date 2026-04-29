import messages.messages as messages

def run(data: dict) -> tuple[bool, str]:
    """
    Inspeciona o payload de criação de modelo de forma ESTRITA (Whitelisting).
    Bloqueia qualquer campo não documentado e valida as restrições matemáticas do Keras.
    """
    operation_name = 'model_create'
    
    allowed_root_keys = {'learning_type', 'architecture', 'training_config', 'rl_params'}
    for key in data.keys():
        if key not in allowed_root_keys:
            err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
            return False, err.replace('{details}', f"Unexpected root key: '{key}'")

    if 'learning_type' not in data:
        return False, messages.MISSING_FIELDS.replace('{operation}', operation_name)
    
    if not isinstance(data['learning_type'], str):
        err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
        return False, err.replace('{details}', "'learning_type' must be a string")

    if 'architecture' not in data:
        return False, messages.MISSING_FIELDS.replace('{operation}', operation_name)
    
    architecture = data['architecture']
    if not isinstance(architecture, dict):
        err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
        return False, err.replace('{details}', "'architecture' must be a dictionary")

    if 'layers' not in architecture or not isinstance(architecture['layers'], list):
        err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
        return False, err.replace('{details}', "The 'architecture' must contain an array of 'layers'")
    
    if len(architecture['layers']) == 0:
        err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
        return False, err.replace('{details}', "The network must have at least one layer")

    allowed_layer_keys = {'type', 'units', 'input_shape', 'activation'}
    allowed_layer_types = {'dense', 'lstm'} 

    for index, layer in enumerate(architecture['layers']):
        if not isinstance(layer, dict):
            err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
            return False, err.replace('{details}', f"Layer at index {index} must be a dictionary")

        for key in layer.keys():
            if key not in allowed_layer_keys:
                err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
                return False, err.replace('{details}', f"Unexpected parameter '{key}' in layer {index}")

        if 'type' not in layer:
            err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
            return False, err.replace('{details}', f"Layer {index} is missing 'type'")
            
        if not isinstance(layer['type'], str) or layer['type'].lower() not in allowed_layer_types:
            err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
            return False, err.replace('{details}', f"Layer {index} 'type' must be one of {allowed_layer_types}")
        
        if 'units' not in layer:
            err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
            return False, err.replace('{details}', f"Layer {index} is missing 'units'")
            
        if type(layer['units']) is not int or layer['units'] <= 0:
            err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
            return False, err.replace('{details}', f"Layer {index} 'units' must be a strictly positive integer")
            
        if index == 0:
            if 'input_shape' not in layer:
                err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
                return False, err.replace('{details}', "The first layer (index 0) MUST contain an 'input_shape' array")
                
            if not isinstance(layer['input_shape'], list) or len(layer['input_shape']) == 0:
                err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
                return False, err.replace('{details}', "The 'input_shape' must be a non-empty array of integers")
            
            for dim in layer['input_shape']:
                if type(dim) is not int or dim <= 0:
                    err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
                    return False, err.replace('{details}', "All dimensions in 'input_shape' must be positive integers")
        else:
            if 'input_shape' in layer:
                err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
                return False, err.replace('{details}', f"Layer {index} should NOT have an 'input_shape'. Only the first layer defines the entry tensor.")

    if 'training_config' in data and not isinstance(data['training_config'], dict):
         err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
         return False, err.replace('{details}', "'training_config' must be a dictionary")

    if 'rl_params' in data and not isinstance(data['rl_params'], dict):
         err = messages.VALIDATION_ERROR.replace('{operation}', operation_name)
         return False, err.replace('{details}', "'rl_params' must be a dictionary")

    return True, None