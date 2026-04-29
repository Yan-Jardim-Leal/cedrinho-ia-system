import sys
import time
import route_manager
import data_manager

from port_manager import PortManager

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL

DEFAULT_PORT = 12345
BUFFER_SIZE = 8192
active_models = {}
active_sessions = {}

def consoleLog(data, address, verbose=False):
    if verbose:
        print(f"[E] {address} [D] {data}")

def processData(data, address, verbose=False):
    consoleLog(data, address, verbose)
    return route_manager.run(data, address, active_models, active_sessions, verbose)

def startServer():
    port = DEFAULT_PORT
    ip = '0.0.0.0'
    verbose = '-v' in sys.argv
    port = '--port' in sys.argv and sys.argv[sys.argv.index('--port') + 1] or DEFAULT_PORT
    
    data_manager.run()
    server = PortManager(ip, port, verbose, BUFFER_SIZE)
    
    print(f"[S] server started and operating asynchronously on {"custom" if '--port' in sys.argv else "default"}  port {port}.")
    server.listenPort(lambda data, address: processData(data, address, verbose))
    if verbose:
        print("\n[V] Debug mode active.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.closeConnections()
        print("\n[S] server process terminated by the operator.")

if __name__ == "__main__":
    startServer()