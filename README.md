# CEDRI - Artificial Intelligence Manager (REST API Edition)

Welcome to the CEDRI Artificial Intelligence Manager! While the tech world often focuses on massive, complex Large Language Models (LLMs), practical applications frequently require lightweight, highly specialized AI models designed for specific tasks. 

My goal is to facilitate the development of AI models for robotics, sensor data processing, and other real-world applications where efficiency and simplicity are key.

This project focuses on users who want to use and train robots in real-time, process sensor data on the fly, or simply experiment with AI without the overhead of massive LLMs. It provides a streamlined **REST API** for creating, loading, saving, training, and running inference on custom neural networks built with TensorFlow/Keras.

There is not many projects out there that offer training at the same time as inference on the same model, and this is one of the main features of this project. You can create a model, load it into RAM, and then send data for both inference and training in real-time, all through simple requests.

- **Modern REST Architecture**: Powered by **FastAPI** and **Uvicorn**, providing highly scalable, asynchronous HTTP endpoints.
- **Auto-Generated Documentation**: Explore and test the API instantly via the built-in interactive Swagger UI.
- **Strict Data Validation**: Features an integrated validation module using **Pydantic V2** that ensures your neural network configurations and hyperparameters are perfectly structured *before* processing begins.
- **Aggressive Memory Management**: Secure model unloading operations that explicitly trigger the Python Garbage Collector to free up RAM instantly.
- **Hybrid Persistence**: Smart storage that keeps metadata in a structured database (SQLite) while handling the physical serialization of models (`.keras` format) within the file system.

---

# 1. Install Guide
To get started with the CEDRI Artificial Intelligence Manager, follow these steps:

1. **Clone the Repository**: Start by cloning the project repository to your local machine using the following command:
```bash
git clone https://github.com/Yan-Jardim-Leal/cedrinho-ia-system.git
cd cedrinho-ia-system/src
```

2. **Install Dependencies**: Install the required dependencies (TensorFlow, FastAPI, Uvicorn, Pydantic) using pip:
```bash
pip install -r requirements.txt
```

3. **Run the Server**: Start the ASGI server using Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 12345 --reload
```
   
4. **Access the Interactive API**: You don't need Telnet or a custom client anymore! Open your browser and navigate to:
   **`http://localhost:12345/docs`**
   Here you will find the interactive Swagger UI where you can visually test all endpoints, see schemas, and send JSON payloads.

---

# 2. How to Create a Model

This documentation provides a step-by-step guide on how to bring a new AI model to life. You simply send a `POST` request with a JSON payload to the `/api/models/create` endpoint.

**Endpoint:** `POST /api/models/create`

## 2.1. Parameters Table

| Field | Hierarchical Location | Mandatory? | Data Type | Observation / Description |
| :--- | :--- | :---: | :---: | :--- |
| `learning_type` | Root | **Yes** | `String` | Learning paradigm. Accepted options: `"supervised"`, `"reinforcement"`, `"predictive_coding"`. |
| `architecture` | Root | **Yes** | `Object` | Block that defines the morphological structure of the neural network. |
| `initializer` | `architecture` | Optional | `String` | Weight initialization algorithm. Example: `"glorot_uniform"`. |
| `layers` | `architecture` | **Yes** | `Array` | Sequential list containing the dictionaries for each layer. Must have a size > 0. |
| `type` | `layers[n]` | **Yes** | `String` | The mathematical type of the layer. Supported options: `"Dense"`, `"LSTM"`. |
| `units` | `layers[n]` | **Yes** | `Integer` | Number of neurons in the layer. Must be a strictly positive integer (> 0). |
| `input_shape` | `layers[0]` | **Yes** | `Array` | Defines the dimension of the input tensor (Ex: `[10]` or `[10, 1]`). **Mandatory only in the index 0 layer.** If sent in other layers, it will cause a validation error. |
| `activation` | `layers[n]` | Optional | `String` | Non-linear activation function of the layer. Common options: `"relu"`, `"tanh"`, `"linear"`, `"sigmoid"`. |
| `training_config` | Root | Optional | `Object` | Configuration block for the compilation engine. |
| `optimizer` | `training_config` | Optional | `String` | Gradient descent algorithm. Example: `"adam"`, `"sgd"`, `"rmsprop"`. |
| `learning_rate` | `training_config` | Optional | `Float` | Learning rate (gradient step). Example: `0.001`. |
| `loss_function` | `training_config` | Optional | `String` | Cost/loss function to evaluate the error. Example: `"mse"`, `"huber"`, `"categorical_crossentropy"`. |
| `metrics` | `training_config` | Optional | `Array` | List of metric strings to be monitored. Example: `["accuracy"]`. |
| `rl_params` | Root | Optional | `Object` | Exclusive block for parameters if `learning_type` is `"reinforcement"`. |
| `gamma` | `rl_params` | Optional | `Float` | Discount Factor. Determines the weight of future vs. present rewards. |
| `epsilon_initial` | `rl_params` | Optional | `Float` | Initial value of the exploration rate in the Epsilon-Greedy policy. |
| `epsilon_decay` | `rl_params` | Optional | `Float` | Multiplicative factor to reduce epsilon over time (Decay). Ex: `0.995`. |
| `buffer_size` | `rl_params` | Optional | `Integer` | Maximum size of the Replay Buffer to store experiences. Ex: `10000`. |

## 2.2. JSON Example: The Most Complex Possible
This example demonstrates a hybrid network (Dense + LSTM) for robotics, with detailed training configurations and RL parameters.

```json
{
  "learning_type": "reinforcement",
  "architecture": {
    "layers": [
      {
        "type": "Dense",
        "units": 64,
        "input_shape": [10, 1]
      },
      {
        "type": "LSTM",
        "units": 32
      },
      {
        "type": "Dense",
        "units": 4
      }
    ]
  },
  "training_config": {
    "optimizer": "adam",
    "learning_rate": 0.0005,
    "loss_function": "huber",
    "metrics": ["accuracy"]
  },
  "rl_params": {
    "gamma": 0.99,
    "epsilon_initial": 1.0,
    "epsilon_decay": 0.995,
    "buffer_size": 50000
  }
}
```

## 2.3. Server Response (Success case)
```json
{
  "message" : "Model created successfully.", 
  "token" : "c5bbb6ce-c023-4a36-a8bc-656df223ea42", 
  "error" : false 
}
```

---

# 3. How to Load and Check a Model

When you create a model, you receive a **token** (UUID). This token is required for all subsequent operations. Before processing data, the model must be loaded into the system's RAM.

## 3.1. Requesting a 'model_load'
**Endpoint:** `POST /api/models/load`

```json
{
  "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42"
}
```

### Success Response
```json
{
  "message": "Model loaded into RAM successfully.",
  "error": false
}
```

## 3.2. Requesting a 'model_check'
**Endpoint:** `POST /api/models/check`
Checks if your model is currently loaded in RAM, its training progress, and database status.

```json
{
  "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42"
}
```

### Success Response
```json
{
  "message": "Model current status: trained",
  "error": false,
  "training_remaining": 0,
  "loaded": true,
  "last_trained": "2026-06-01 12:34:56"
}
```

---

# 4. How to Use a Model

These endpoints require the model to be actively loaded in memory.

## 4.1. Requesting a 'model_process' (Inference)
**Endpoint:** `POST /api/models/process`
Use this to pass sensor data or environment states through the network and get a prediction.

```json
{
  "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42",
  "input": [1.5, 2.3, 0.8], 
  "session_id": "session-XYZ-123"
}
```

### Success Response
```json
{
  "message": "Model processed successfully.",
  "error": false,
  "output": [0.89, -0.12],
  "session_id": "session-XYZ-123"
}
```

## 4.2. Requesting a 'model_train'
**Endpoint:** `POST /api/models/train`
Provides the network with an array of experiences or labeled data to adjust its internal weights.

```json
{
  "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42",
  "session_id": "session-XYZ-123",
  "train_data": [
    {
      "state": [1.5, 0.2],
      "action": [1.0, 0.0],
      "reward": 10.5,
      "next_state": [1.6, 0.2],
      "done": false
    }
  ],
  "epochs": 1
}
```

### Success Response
```json
{
  "message": "Successfully processed and trained on 1 experience steps.",
  "error": false,
  "session_id": "session-XYZ-123"
}
```

---

# 5. Advanced Operations

## 5.1. Requesting a 'model_update'
**Endpoint:** `POST /api/models/update`
Dynamically update hyperparameters (like learning rate) on the fly without recreating the model.

```json
{
  "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42",
  "updates": {
    "learning_rate": 0.0005, 
    "epsilon": 0.1
  }
}
```

## 5.2. Requesting a 'model_unload'
**Endpoint:** `POST /api/models/unload`
Neural networks consume significant RAM. If you are not using a model, you should unload it. Our unload system aggressively forces Python's Garbage Collector to free the RAM/VRAM allocations immediately.

```json
{
  "token": "c5bbb6ce-c023-4a36-a8bc-656df223ea42"
}
```

### Success Response
```json
{
  "message": "Model aggressively unloaded. :)",
  "error": false
}
```

---

## Important Facts:
**Security Warning:** Never expose this project directly to the public internet on an open system port. In a production environment, always deploy this FastAPI application behind a secure Reverse Proxy (such as Nginx or Traefik) and utilize HTTPS (TLS/SSL) certificates to encrypt the JSON payloads (like the IPB campus network).

## Fun facts: How they do it?
All neural networks can be summarized by mathematical formulas, ranging from the simplest to the most complex. With this in mind, the job of programming neural networks fundamentally comes down to translating these mathematical formulas into code, such as summations, divisions, and multiplications. This project uses a library called TensorFlow as its main engine. They have already done the overwhelming majority of the heavy lifting by translating the most important and market-standard mathematical formulas into optimized C++ backend code for your project.

## License
This project is licensed under the MIT License.

Creator: **Yan Jardim Leal** <br>Institution: **Polytechnic Institute of Bragança (IPB)**