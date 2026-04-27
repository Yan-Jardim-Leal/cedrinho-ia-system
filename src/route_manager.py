import json
import messages.messages as messages
import model.create as create
import model.load as load
import model.train as train
import model.process as process

def run(data, address, active_models, active_sessions, verbose=False):

    try:
        recieved_json = json.loads(data)
        if 'operation' not in recieved_json or 'data' not in recieved_json:
            return messages.MISSING_FIELDS.replace('{operation}', recieved_json.get('operation', ''))

        # Temos a operação, agora vamos ver qual é a operação
        operation = recieved_json['operation']
        if operation == 'echo':
            return recieved_json['data']
        elif operation == 'model_create':
            return create.run(recieved_json['data'])
        elif operation == 'model_load':
            return load.run(recieved_json['data'], active_models)
        elif operation == 'model_train':
            return train.run(recieved_json['data'], active_models, active_sessions)
        elif operation == 'model_process':
            return process.run(recieved_json['data'], active_models, active_sessions)
        elif operation == 'model_check':
            return check.run(recieved_json['data'])
        else:
            return messages.INVALID_OPERATION.replace('{operation}', operation)

    except json.JSONDecodeError:
        return messages.INVALID_JSON

    return data