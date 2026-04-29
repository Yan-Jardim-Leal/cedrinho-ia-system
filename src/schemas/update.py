from pydantic import BaseModel, Field
from typing import Optional

# ==========================================
# SUB-SCHEMA
# ==========================================
class UpdateHyperparameters(BaseModel):
    learning_rate: Optional[float] = Field(None, title="Learning Rate", description="New learning rate for the optimizer.")
    epsilon: Optional[float] = Field(None, title="Epsilon", description="New exploration rate for Epsilon-Greedy policies.")
    mutation_rate: Optional[float] = Field(None, title="Mutation Rate", description="New mutation rate (if applicable for genetic/evolutionary approaches).")

# ==========================================
# REQUEST SCHEMA
# ==========================================
class ModelUpdateValidator(BaseModel):
    token: str = Field(
        ..., 
        title="Token", 
        description="Unique identifier token of the model to update."
    )
    updates: UpdateHyperparameters = Field(
        ..., 
        title="Hyperparameter Updates", 
        description="Dictionary containing the hyperparameter keys and new values to update on the fly."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42",
                    "updates": {
                        "learning_rate": 0.0005,
                        "epsilon": 0.1,
                        "mutation_rate": 0.02
                    }
                }
            ]
        }
    }

# ==========================================
# RESPONSE SCHEMA
# ==========================================
class ModelUpdateResponse(BaseModel):
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