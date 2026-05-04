import argparse
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import data_manager

from schemas.create  import ModelCreateValidator, ModelCreateResponse
from schemas.load    import ModelLoadValidator, ModelLoadResponse
from schemas.update  import ModelUpdateValidator, ModelUpdateResponse
from schemas.check   import ModelCheckValidator, ModelCheckResponse
from schemas.unload  import ModelUnloadValidator, ModelUnloadResponse
from schemas.train   import ModelTrainValidator, ModelTrainResponse
from schemas.process import ModelProcessValidator, ModelProcessResponse
from schemas.check   import ModelCheckValidator, ModelCheckResponse
from schemas.unload  import ModelUnloadValidator, ModelUnloadResponse

from model import check, load, create, train, process

active_models = {}
active_sessions = {}

config = {
    "verbose": False,
    "port": 48050
}

async def lifespan(app: FastAPI):
    """Chamada inicial, inicia o servidor e os subsistemas necessários."""
    if config["verbose"]:
        print(f"[S] starting IA Manager with Verbose Mode ON...")
        print(f"[S] Configurações de Rede: PORT={config['port']}")
    else:
        print("[S] starting IA Manager...")
        
    data_manager.run()
    yield
    print("[S] stopping IA Manager...")

app = FastAPI(
    title="CEDRI IA Manager",
    description="REST API for the CEDRI IA MANAGER from IPB",
    version="2.0.0",
    lifespan=lifespan
)

# ==========================================
#       ROTAS REST
# ==========================================

@app.get("/api/echo")
async def echo_route():
    return {"message": "[S] Server loaded."}

@app.post("/api/models/create", status_code=200, response_model=ModelCreateResponse)
async def create_model_route(payload: ModelCreateValidator):
    """Model creation endpoint. Expects a JSON payload with model configuration parameters."""
    result = create.run(payload.model_dump())
    return result

@app.post("/api/models/load", status_code=200, response_model=ModelLoadResponse)
async def load_model_route(payload: ModelLoadValidator):
    """Load a model into active memory (RAM) using the provided token. Expects a JSON payload with the model token."""
    result = load.run(payload.model_dump(), active_models)
    return result

@app.post("/api/models/train", status_code=200, response_model=ModelTrainResponse)
async def train_model_route(payload: ModelTrainValidator):
    """Train a loaded model using the provided token and training data. Expects a JSON payload with the model token and training data."""
    result = train.run(payload.model_dump(), active_models, active_sessions)
    return result

@app.post("/api/models/process", status_code=200, response_model=ModelProcessResponse)
async def process_model_route(payload: ModelProcessValidator):
    """Process input data through a loaded model using the provided token. Expects a JSON payload with the model token and input data."""
    result = process.run(payload.model_dump(), active_models, active_sessions)
    return result

@app.post("/api/models/check", status_code=200, response_model=ModelCheckResponse)
async def check_model_route(payload: ModelCheckValidator):
    """Check the status of a model using the provided token. Expects a JSON payload with the model token."""
    result = check.run(payload.model_dump())
    return result

@app.post("/api/models/unload", status_code=200, response_model=ModelUnloadResponse)
async def unload_model_route(payload: ModelUnloadValidator):
    """Unload a model from active memory (RAM) using the provided token. Expects a JSON payload with the model token."""
    result = load.run(payload.model_dump(), active_models)
    return result

# ==========================================
#       INICIALIZAÇÃO
# ==========================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CEDRI IA Manager Startup Script")
    
    parser.add_argument("-v", "--verbose", action="store_true", help="Activate detailed loggings.")
    parser.add_argument("--port", type=int, default=48050, help="Porta do servidor da IA (padrão: 48050)")
    
    args = parser.parse_args()
    
    config["verbose"] = args.verbose
    config["port"] = args.port
    
    print(f"[S] Iniciando o servidor Uvicorn na porta {args.port}...")
    
    uvicorn.run(app, host="0.0.0.0", port=args.port)