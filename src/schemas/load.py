from pydantic import BaseModel, Field

# ==========================================
# REQUEST SCHEMA
# ==========================================
class ModelLoadValidator(BaseModel):
    token: str = Field(
        ..., 
        title="Token", 
        description="Unique identifier token to load the model into the system's active memory (RAM)."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42"
                }
            ]
        }
    }

# ==========================================
# RESPONSE SCHEMA
# ==========================================
class ModelLoadResponse(BaseModel):
    message: str = Field(
        ..., 
        title="Message", 
        description="Success or error message."
    )
    error: bool = Field(
        ..., 
        title="Error Flag", 
        description="Indicates if the operation failed."
    )