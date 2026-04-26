def validate_model_create(data: dict) -> tuple[bool, str]:
    """
    Inspeciona o payload de criação de modelo.
    Retorna uma tupla (Valido: bool, Motivo: str).
    """
    if 'learning_type' not in data:
        return False, "Missing required field: 'learning_type'"
    
    if 'architecture' not in data:
        return False, "Missing configuration block: 'architecture'"
    
    architecture = data['architecture']
    if 'layers' not in architecture or not isinstance(architecture['layers'], list):
        return False, "A 'arcitecture' must contain a array of 'layers'"
    
    if len(architecture['layers']) == 0:
        return False, "The network must have at least one layer"

    for index, layer in enumerate(architecture['layers']):
        if 'type' not in layer:
            return False, f"Layer at index {index} is missing 'type' (e.g., Dense, LSTM)"
        if 'units' not in layer:
            return False, f"Layer at index {index} is missing 'units'"
        if not isinstance(layer['units'], int):
            return False, f"The value of 'units' in layer {index} must be an integer"

    if 'training_config' not in data:
        return False, "Missing 'training_config' block"
    
    return True, "Validation successful"