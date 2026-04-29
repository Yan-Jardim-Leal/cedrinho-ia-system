import json
import messages.messages as messages

from model import check, load, create, train, process
from validator import val_check, val_create, val_process, val_train, val_load

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
            validation = val_create.run(recieved_json['data'])
            if not validation[0]:
                return validation[1]
            return create.run(recieved_json['data'])
        elif operation == 'model_load':
            validation = val_load.run(recieved_json['data'])
            if not validation[0]:
                return validation[1]
            return load.run(recieved_json['data'], active_models)
        elif operation == 'model_train':
            validation = val_train.run(recieved_json['data'])
            if not validation[0]:
                return validation[1]
            return train.run(recieved_json['data'], active_models, active_sessions)
        elif operation == 'model_process':
            validation = val_process.run(recieved_json['data'])
            if not validation[0]:
                return validation[1]
            return process.run(recieved_json['data'], active_models, active_sessions)
        elif operation == 'model_check':
            validation = val_check.run(recieved_json['data'])
            if not validation[0]:
                return validation[1]
            return check.run(recieved_json['data'])
        else:
            return messages.INVALID_OPERATION.replace('{operation}', operation)

    except json.JSONDecodeError:
        return messages.INVALID_JSON

    return data