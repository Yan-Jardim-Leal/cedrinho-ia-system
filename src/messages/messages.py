# Respostas de erro
INVALID_JSON = '{"operation" : "", "data" : { "message" : "Invalid JSON format", "error" : true } }'
INVALID_OPERATION = '{"operation" : "{operation}", "data" : { "message" : "Invalid operation", "error" : true } }'
MISSING_FIELDS = '{"operation" : "{operation}", "data" : { "message" : "Missing required fields", "error" : true } }'
INTERNAL_ERROR = '{"operation" : "{operation}", "data" : { "message" : "Internal error: {details}", "error" : true } }'
RAM_ERROR = '{"operation" : "{operation}", "data" : { "message" : "Model not loaded in RAM", "error" : true } }'
VALIDATION_ERROR = '{"operation" : "{operation}", "data" : { "message" : "Validation Error: {details}", "error" : true } }'

# Respostas de sucesso
MODEL_CREATED = '{"operation" : "model_create", "data" : { "message" : "Model created successfully", "token" : "{token}", "error" : false } }'
MODEL_LOADED = '{"operation" : "model_load", "data" : { "message" : "Model is now loading, use check for details", "error" : false } }'
MODEL_TRAINED = '{"operation" : "model_train", "data" : { "message" : "Model trained successfully", "session_id" : "{session_id}", "error" : false } }'
MODEL_PROCESSED = '{"operation" : "model_process", "data" : { "message" : "Model processed successfully", "session_id" : "{session_id}", "output" : "{output}", "error" : false } }'

SUCCESS = 1
ERROR = 0