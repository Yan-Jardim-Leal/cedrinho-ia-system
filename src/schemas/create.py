from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Literal

# ==========================================
# SUB-SCHEMAS
# ==========================================

class LayerConfig(BaseModel):
    type: Literal["Dense", "LSTM"]      = Field(..., description="Mathematical type of the layer")
    units: int                          = Field(..., gt=0, description="Number of neurons (> 0)")
    input_shape: Optional[List[int]]    = Field(None, description="Dimension of the input tensor")
    activation: Optional[str]           = Field(None, description="Non-linear activation function")

class ArchitectureConfig(BaseModel):
    initializer: Optional[str]  = Field("glorot_uniform", description="Initialization algorithm")
    layers: List[LayerConfig]   = Field(..., min_length=1)

    @model_validator(mode='after')
    def validate_input_shape(self) -> 'ArchitectureConfig':
        for i, layer in enumerate(self.layers):
            if i == 0:
                if layer.input_shape is None:
                    raise ValueError("The 'input_shape' field is required in the first layer (index 0).")
            else:
                if layer.input_shape is not None:
                    raise ValueError(f"The 'input_shape' field is forbidden in subsequent layers (index {i}). Keras infers it automatically.")
        return self

class TrainingConfig(BaseModel):
    optimizer       : Optional[str]       = Field(None, description="Ex: adam, sgd")
    learning_rate   : Optional[float]     = Field(None, description="Gradient step")
    loss_function   : Optional[str]       = Field(None, description="Cost function")
    metrics         : Optional[List[str]] = Field(None, description="Monitored metrics")

class RLParams(BaseModel):
    gamma           : Optional[float] = Field(None, description="Discount factor")
    epsilon_initial : Optional[float] = Field(None, description="Initial exploration rate")
    epsilon_decay   : Optional[float] = Field(None, description="Decay factor")
    buffer_size     : Optional[int]   = Field(None, description="Replay Buffer size")

# ==========================================
# MAIN SCHEMA (REQUEST)
# ==========================================

class ModelCreateValidator(BaseModel):
    learning_type: Literal["supervised", "reinforcement", "predictive_coding"]
    architecture: ArchitectureConfig
    training_config: Optional[TrainingConfig] = None
    rl_params: Optional[RLParams] = None

    @model_validator(mode='after')
    def validate_rl_params_context(self) -> 'ModelCreateValidator':
        if self.learning_type == "reinforcement" and self.rl_params is None:
            raise ValueError("The learning_type is 'reinforcement', it is highly recommended to provide 'rl_params'.")
        if self.learning_type != "reinforcement" and self.rl_params is not None:
            raise ValueError(f"The 'rl_params' block must not be sent for the learning_type '{self.learning_type}'.")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "learning_type": "supervised",
                    "architecture": {
                        "layers": [
                            {"type": "Dense", "units": 64, "input_shape": [10], "activation": "relu"},
                            {"type": "Dense", "units": 2, "activation": "linear"}
                        ]
                    },
                    "training_config": {
                        "optimizer": "adam",
                        "learning_rate": 0.001,
                        "loss_function": "mse"
                    }
                }
            ]
        }
    }

# ==========================================
# RESPONSE SCHEMA (WHAT IS RETURNED)
# ==========================================

class ModelCreateResponse(BaseModel):
    message: str = Field(
        ..., 
        title="Status Message", 
        description="Success or error message."
    )
    token: Optional[str] = Field(
        None, 
        title="Model Token", 
        description="Unique UUID token generated for the model."
    )
    error: bool = Field(..., 
        title="Error Flag", 
        description="Boolean indicating whether the operation failed."
    )