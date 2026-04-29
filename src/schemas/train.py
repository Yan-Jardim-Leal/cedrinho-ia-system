from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# SUB-SCHEMA
# ==========================================
class TrainDataStep(BaseModel):
    state: List[float] = Field(..., title="Current State", description="The environment observation array before taking the action.")
    action: List[float] = Field(..., title="Action Taken", description="The numerical representation of the action taken by the agent.")
    reward: float = Field(..., title="Reward", description="The numerical reward received after taking the action.")
    next_state: List[float] = Field(..., title="Next State", description="The resulting environment observation array after the action was taken.")
    done: bool = Field(..., title="Is Done", description="Boolean flag indicating if the episode or training sequence has ended.")

# ==========================================
# REQUEST SCHEMA
# ==========================================
class ModelTrainValidator(BaseModel):
    token: str = Field(
        ..., 
        title="Token", 
        description="Unique identifier token of the model to be trained."
    )
    session_id: str = Field(
        ..., 
        title="Session", 
        description="Unique identifier linking this training data to a specific active session."
    )
    train_data: List[TrainDataStep] = Field(
        ..., 
        title="Training Data", 
        description="List of experience steps containing state transitions and rewards for the training queue."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42",
                    "session_id": "session-XYZ-123",
                    "train_data": [
                        {
                            "state": [1.5, 0.2],
                            "action": [1.0, 0.0],
                            "reward": 10.5,
                            "next_state": [1.6, 0.2],
                            "done": False
                        }
                    ]
                }
            ]
        }
    }

# ==========================================
# RESPONSE SCHEMA
# ==========================================
class ModelTrainResponse(BaseModel):
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
    session_id: Optional[str] = Field(
        None, 
        title="Session ID", 
        description="The session identifier provided in the request."
    )