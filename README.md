# CEDRI - Artificial Intelligence Manager

Welcome to the CEDRI Artificial Intelligence Manager! While the tech world often focuses on massive, complex Large Language Models (LLMs), practical applications frequently require lightweight, highly specialized AI models designed for specific tasks. 

My goal is to facilitade the development of IA models for robotics, sensor data processing, and other real-world applications where efficiency and simplicity are key.

This main project focus is for who wants to use and train robots in real-time, you can also process sensor data on the fly, or simply experiment with AI without the overhead of massive LLMs. It provides a streamlined interface for creating, loading, saving, training, and running inference on custom neural networks built with Keras.

- **Communication Management**: Utilizes the `port-manager` library to efficiently handle asynchronous TCP connections.
- **Operations Protocol**: Native, out-of-the-box support for creating, loading, saving, training, and running model inference.
- **Data Security**: Features an integrated validation module that ensures your neural network configurations and hyperparameters are perfectly structured before processing begins.
- **Hybrid Persistence**: Smart storage that keeps metadata in a structured database while handling the physical serialization of models within the file system.

---

# 1. Instalation guide
To get started with the CEDRI Artificial Intelligence Manager, follow these steps:
1. **Clone the Repository**: Start by cloning the project repository to your local machine using the following command:
   ```bash
   git clone https://github.com/Yan-Jardim-Leal/cedrinho-ia-system/tree/main
    ```
2. **Navigate to the Project Directory**: 
    Change your current directory to the project folder:
   ```bash
   cd cedri-ai-manager
   ```
3. **Install Dependencies**: Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Server**: Start the server using the following command:
   ```bash
   python server.py --port 12345 -v
   ```
   
5. **Connect to the Server**: You can now connect to the server using a TCP client (e.g., `telnet`, `netcat`, or a custom client application) to send JSON payloads for model creation, loading, training, and inference.

# 2. How to Create a Model

This documentation provides a step-by-step guide on how to bring a new AI model to life. To do this, you simply send a JSON payload to the server containing the required and optional configurations. Below is a comprehensive guide to understanding and using these AI-related variables.

## 2.1. Parameters Table

| Field | Hierarchical Location | Mandatory? | Data Type | Observation / Description |
| :--- | :--- | :---: | :---: | :--- |
| `operation` | Root | **Yes** | `String` | Must be exactly `"model_create"`. |
| `data` | Root | **Yes** | `Object` | Main dictionary containing the model payload. |
| `learning_type` | `data` | **Yes** | `String` | Learning paradigm. Accepted options: `"supervised"`, `"reinforcement"`, `"predictive_coding"`. |
| `architecture` | `data` | **Yes** | `Object` | Block that defines the morphological structure of the neural network. |
| `initializer` | `architecture` | Optional | `String` | Weight initialization algorithm. Example: `"glorot_uniform"`. |
| `layers` | `architecture` | **Yes** | `Array` | Sequential list containing the dictionaries for each layer. Must have a size > 0. |
| `type` | `layers[n]` | **Yes** | `String` | The mathematical type of the layer. Supported options: `"Dense"`, `"LSTM"`. |
| `units` | `layers[n]` | **Yes** | `Integer` | Number of neurons in the layer. Must be a strictly positive integer (> 0). |
| `input_shape` | `layers[0]` | **Yes** | `Array` | Defines the dimension of the input tensor (Ex: `[10]` or `[10, 1]`). **Mandatory only in the index 0 layer.** If sent in other layers, it will cause a validation error. |
| `activation` | `layers[n]` | Optional | `String` | Non-linear activation function of the layer. Common options: `"relu"`, `"tanh"`, `"linear"`, `"sigmoid"`. |
| `training_config` | `data` | Optional | `Object` | Configuration block for the compilation engine (`.keras` compilation). |
| `optimizer` | `training_config` | Optional | `String` | Gradient descent algorithm. Example: `"adam"`, `"sgd"`, `"rmsprop"`. |
| `learning_rate` | `training_config` | Optional | `Float` | Learning rate (gradient step). Example: `0.001`. |
| `loss_function` | `training_config` | Optional | `String` | Cost/loss function to evaluate the error. Example: `"mse"`, `"huber"`, `"categorical_crossentropy"`. |
| `metrics` | `training_config` | Optional | `Array` | List of metric strings to be monitored. Example: `["accuracy", "reward_mean"]`. |
| `rl_params` | `data` | Optional | `Object` | Exclusive block for parameters if `learning_type` is `"reinforcement"`. |
| `gamma` | `rl_params` | Optional | `Float` | Discount Factor. Determines the weight of future vs. present rewards. |
| `epsilon_initial` | `rl_params` | Optional | `Float` | Initial value of the exploration rate in the Epsilon-Greedy policy. |
| `epsilon_decay` | `rl_params` | Optional | `Float` | Multiplicative factor to reduce epsilon over time (Decay). Ex: `0.995`. |
| `buffer_size` | `rl_params` | Optional | `Integer` | Maximum size of the Replay Buffer to store experiences. Ex: `10000`. |

---

## 2.2. How the Variables Work (And Why You Need Them)

This section explains what each parameter does inside the AI's "brain", why it was included in our architecture, and what options are available to you. 

### Root Level (The Message Envelope)
Think of this as an email you are sending to the server.
* **`operation`**: The "subject line" of your message. To create a model, this must always be `"model_create"`. If you send anything else, the internal router will redirect your payload to the wrong system.
* **`data`**: The "body" of the email. This is a JSON object (dictionary) that packages all the actual configurations the Keras engine needs to build your AI.

### Level: `data` (Global Configurations)
* **`learning_type`**: Defines the "philosophy" of how the model will learn. 
    * **Options**: `"supervised"` (learns from examples using an answer key), `"reinforcement"` (learns by interacting with an environment, earning "points" through trial and error), `"predictive_coding"` (experimental).
    * **Background**: CEDRI handles diverse challenges. Classifying sensor images requires supervised learning, but teaching a robotic arm to navigate an obstacle course requires reinforcement learning. This variable tells the server which strategy to prepare.

### Level: `architecture` (The Model's Skeleton)
This block defines how the network's neurons are structured and connected.
* **`initializer`** *(Optional)*: Defines how the "weights" (the AI's foundational knowledge) begin. If left blank, Keras applies a default.
    * **Example**: `"glorot_uniform"`.
    * **Why it exists**: An AI isn't born knowing everything, but it can't be born completely "empty" either (all zeros prevent the math from working). It starts with random values. The initializer is the mathematical algorithm that generates this initial randomness in an optimized, balanced way.
* **`layers`**: A list of dictionaries, processed from top to bottom. Think of each item as a "checkpoint" or "filter" the data must pass through.

### Level: `layers` (The Neurons)
* **`type`**: The structural format of the layer.
    * **`Dense`**: Every neuron connects to every neuron in the previous layer. This is the standard, go-to layer for most tasks.
    * **`LSTM`**: A layer with "memory." Excellent for analyzing sensor data over time (time-series), where the past influences the present.
    * **`Transformers`**: Uses a mechanism called "Self-Attention" to mathematically calculate how strongly each value in a array relates to every other value, instantly mapping out the entire context.
* **`units`**: The number of neurons in that specific layer. The higher the number, the smarter and more complex the model becomes—but it will also run slower and demand more RAM.
* **`input_shape`**: **(MANDATORY ONLY FOR THE FIRST LAYER)**. The mathematical dimensions of the data the model should expect to receive.
    * **Example**: `[10]` means the AI should expect exactly 10 sensor readings per input.
    * **Why it exists**: The underlying engine (TensorFlow) cannot build the network's architecture without knowing the size of the "front door." If you try to define this in middle layers, the system will block it to prevent tensor dimension crashes.
* **`activation`** *(Optional)*: The mathematical function that "filters" what a neuron outputs.
    * **Common Options**: `"relu"`, `"tanh"`, `"linear"`, `"sigmoid"`.
    * **Why it exists**: Without activation functions, a massive 1,000-layer network would mathematically collapse into the equivalent of a single-layer network (just a straight, linear line). Activation functions introduce *non-linearity*, allowing the AI to learn complex patterns, curves, and boundaries.

### Level: `training_config` (The Classroom)
This defines how the AI will be educated when you trigger the `model_train` operation.
* **`optimizer`**: The "teacher" that reviews the AI's mistakes and adjusts its internal weights.
    * **Options**: `"adam"` (the modern industry standard), `"sgd"`, `"rmsprop"`.
* **`learning_rate`**: The "step size" the optimizer takes when correcting the AI.
    * **Why it exists**: If set to `1.0` (a giant step), the model swings wildly, overshoots the answer, and never learns. If set to `0.000001` (a microscopic step), it might take millennia to learn. Standard values (like `0.001`) offer a balanced, steady learning pace.
* **`loss_function`**: The "exam score" that measures exactly how wrong the AI's guesses are. The network's ultimate goal is always to drive this *loss* value down to zero.
    * **Options**: `"mse"` (Mean Squared Error, great for predicting exact numbers), `"huber"` (a hybrid approach that is less distracted by extreme data anomalies/outliers).
* **`metrics`**: The "report card." Unlike the loss function, metrics do not affect how the AI learns; they are simply human-readable numbers translated to help you understand if the model is actually performing well.
    * **Options**: `["accuracy"]` (percentage of correct answers), `["reward_mean"]` (average points earned in robotics/games).

### Level: `rl_params` (The Reinforcement Learning Brain)
*Exclusive to when `learning_type` is set to `"reinforcement"`.* This sets the rules of the environment where your AI agent will operate.
* **`gamma`**: The "foresight" factor (ranges from `0.0` to `1.0`). It dictates whether the AI agent prefers an immediate, small reward or has the patience to plan ahead for a massive reward later on.
* **`epsilon_initial`**: The starting "curiosity" rate. If set to `1.0`, the agent ignores everything it knows and takes 100% random actions to explore its world and discover new strategies.
* **`epsilon_decay`**: The pace of "maturation." At each step, the current epsilon is multiplied by this number (e.g., `0.995`). This ensures the agent starts out highly curious but gradually relies more on its earned experience to make smart decisions.
* **`buffer_size`**: The size of the agent's "hippocampus" (memory). It dictates how many past experiences (e.g., `10000`) are kept in RAM so the AI can continually replay and relearn from its own past successes and failures.

---

## 2.3. JSON Example: The Simplest Possible
This example creates a basic single-layer network to process 2 inputs and generate 1 output.

```json
{
  "operation": "model_create",
  "data": {
    "learning_type": "supervised",
    "architecture": {
      "layers": [
        {
          "type": "Dense",
          "units": 1,
          "input_shape": [2]
        }
      ]
    }
  }
}

```

## 2.4. JSON Example: The Most Complex Possible
This example demonstrates a hybrid network (Dense + LSTM) for robotics, with detailed training configurations and RL parameters.

```json
{
  "operation": "model_create",
  "data": {
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
      "metrics": ["accuracy", "reward"]
    },
    "rl_params": {
      "gamma": 0.99,
      "epsilon_initial": 1.0,
      "epsilon_decay": 0.995,
      "buffer_size": 50000
    }
  }
}
```

## 2.5. Server Response (Success case)
```json
{
    "operation" : "model_create", 
    "data" : { 
        "message" : "Model created successfully", 
        "token" : "created-token", 
        "error" : false 
    } 
}
```
## 2.6. Server Response (Failture case)
```json
{
    "operation" : "model_create", 
    "data" : { 
        "message" : "Error message", 
        "error" : true 
    } 
}

```

# 3. How to Load a Model

Now that we have the basics down, we can finally use the model we created. To interact with it, we have a few specific functions and protocols to send to the server. Let's dive in:

When you created the model, did you notice that you received a token in the response? This token is what you must use for all subsequent operations.

First, before performing any data operations, we must load our model using the `"model_load"` operation. This action loads the model into the system's memory so it is ready for active operations, such as data processing and training.

You can check whether your model is currently loaded or not using the `"model_check"` operation. This operation also provides a wealth of other useful information, such as the training progress of your AI, its current load status, and whether it is actively processing data right now!

## 3.1. Requesting a 'model_check'
```json
{
    "operation" : "model_check",
    "data" : {
        "token" : "created-token"
    }
}
```
### 3.1.1. Success Response
```json
{
    "operation" : "model_check",
    "data" : {
        "message" : "",
        "error" : false,
        "training_remaining" : 0,
        "loaded" : true,
        "last_trained": "2024-06-01T12:34:56Z"
    }
}
```
### 3.1.2. Error Response
```json
{
    "operation" : "model_check",
    "data" : {
        "message" : "No models found with that token",
        "error" : true
    }
}
```
## 3.2. Requesting a 'model_load'
```json
    {
    "operation" : "model_load",
    "data" : {
        "token" : "created-token"
    }
}
```
### 3.2.1. Success Response
```json
{
    "operation" : "model_load",
    "data" : {
        "message" : "Model is now loading, use check for details",
        "error" : false,
    }
}
```
### 3.2.2. Error Response
```json
{
    "operation" : "model_load",
    "data" : {
        "message" : "No models found with that token",
        "error" : true
    }
}
```

---

# 4. How to Use a Model

Now that we know how to load a model, let's look at the operations that require the model to be actively loaded in memory.

## 4.1. Requesting a 'model_process'
When processing a model, we can store a session, this session serves to maintain consistency between multiple requests.
```json
{
    "operation" : "model_process",
    "data" : {
        "token" : "created-token",
        "input" : [1,2,3], 
        "session_id" : "session-XYZ",
    }
}
```
### 4.1.1. Success Response
```json
{
    "operation" : "model_process",
    "data" : {
        "message" : "",
        "error" : false,
        "output" : [1,2,3],
        "session_id" : "session-XYZ",
    }
}
```
### 4.1.2. Error Response
```json
{
    "operation" : "model_process",
    "data" : {
        "message" : "Failed to process",
        "error" : true
    }
}
```

## 4.2. Requesting a 'model_train'
```json
{
    "operation" : "model_train",
    "data" : {
        "token" : "created-token",
        "session_id" : "session-XYZ",
        "train_data" : [{
            "state" : [1.5, 0.2],
            "action" : [1, 0],
            "reward" : 10.5,
            "next_state" : [1.6, 0.2],
            "done" : false
        }]
    }
}
```
### 4.2.1. Success Response
```json
{
    "operation" : "model_train",
    "data" : {
        "message" : "Added to the training queue.",
        "error" : false,
        "session_id" : "session-XYZ",
    }
}
```
### 4.2.2. Error Response
```json
{
    "operation" : "model_train",
    "data" : {
        "message" : "Failed to add to the train queue",
        "error" : true
    }
}
```

---

# 5. Important Operations

Beyond the basic operations of creating, loading, processing, and training models, there are some additional operations that can be very useful for managing your AI models effectively. These operations allow you to update model hyperparameters on the fly and unload models from memory when not in use.

## 5.1. Requesting a 'model_update'
This operation allows you to update the hyperparameters of a model that is currently loaded in memory. This is particularly useful for reinforcement learning models, where you might want to adjust parameters like the learning rate or exploration rate on the fly without having to recreate and retrain the model from scratch.

```json
{
    "operation" : "model_update",
    "data" : {
        "token" : "created-token",
        "updates" : {
            "learning_rate" : 0.0005, 
            "epsilon" : 0.1,          
            "mutation_rate" : 0.02    
        }
    }
}
```
### 5.1.1. Success Response
```json
{
    "operation" : "model_update",
    "data" : {
        "message" : "Model hyperparameters updated successfully.",
        "error" : false
    }
}
```
### 5.2. Requesting a 'model_unload'
Complex models consumes a lot of RAM. If you have multiple models or a model that is too large, you can unload it from memory when you are not using it. This operation does not delete the model, it simply removes it from RAM. You can load it again later when you need it.
```json
{
    "operation" : "model_unload",
    "data" : {
        "token" : "created-token"
    }
}
```
### 5.2.1. Success Response
```json
{
    "operation" : "model_unload",
    "data" : {
        "message" : "Model unloaded from RAM successfully.",
        "error" : false
    }
}
```

---

## Important Facts:
**Security Warning:** This project does not focus on cybersecurity. **Never** expose this project on an open system port directly to the internet. If you want to make it publicly accessible, you must build a secure wrapper around it, as the current architecture was not designed with extensive cybersecurity measures in mind.

## Fun facts: How they do it?

All neuron networks can be summarized by mathematical formulas, ranging from the simplest to the most complex. With this in mind, the job of programming neural networks fundamentally comes down to translating these mathematical formulas into code, such as summations, divisions, and multiplications. This project uses a library called TensorFlow as its main engine. They have already done the overwhelming majority of the heavy lifting by translating the most important and market-standard mathematical formulas into optimized code for your project.

## License
This project is licensed under the MIT License.

Creator: **Yan Jardim Leal**.  
Institution: **Polytechnic Institute of Bragança (IPB)**.
