from pydantic import BaseModel, Field
from typing import Optional

# ==========================================
# REQUEST SCHEMA
# ==========================================
class ModelCheckValidator(BaseModel):
    token: str = Field(
        ..., 
        title="Token", 
        description="Unique identifier token for the model to check its status."
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
class ModelCheckResponse(BaseModel):
    message: str = Field(
        ..., 
        title="Message", 
        description="Status message."
    )
    error: bool = Field(
        ..., 
        title="Error Flag", 
        description="Indicates if the operation failed."
        )
    training_remaining: Optional[int] = Field(
        None, 
        title="Training Remaining", 
        description="Number of items left in the training queue."
    )
    loaded: Optional[bool] = Field(
        None, 
        title="Loaded Status", 
        description="Indicates if the model is currently loaded in RAM."
    )
    last_trained: Optional[str] = Field(
        None, 
        title="Last Trained", 
        description="Timestamp of the last training session."
    )