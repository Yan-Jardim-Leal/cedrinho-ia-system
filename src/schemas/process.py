from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# REQUEST SCHEMA
# ==========================================
class ModelProcessValidator(BaseModel):
    token: str = Field(
        ..., 
        title="Token", 
        description="Unique identifier token of the loaded model to perform inference."
    )
    input: List[float] = Field(
        ..., 
        title="Input Data", 
        description="Array of numerical values (tensor) to be processed by the neural network."
    )
    session_id: str = Field(
        ..., 
        title="Session", 
        description="Unique identifier for the current processing session to maintain state consistency."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42",
                    "input": [1.5, 2.3, 0.8],
                    "session_id": "session-XYZ-123"
                }
            ]
        }
    }

# ==========================================
# RESPONSE SCHEMA
# ==========================================
class ModelProcessResponse(BaseModel):
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
    output: Optional[List[float]] = Field(
        None, 
        title="Model Output", 
        description="Resulting output array from the neural network."
    )
    session_id: Optional[str] = Field(
        None, 
        title="Session ID", 
        description="The session identifier provided in the request."
    )