import sys
import time
import route_manager
import data_manager

from port_manager import PortManager

BUFFER_SIZE = 8192

def consoleLog(data, address, verbose=False):
    if verbose:
        print(f"[E] {address} [D] {data}")

def processData(data, address, verbose=False):
    consoleLog(data, address, verbose)
    return route_manager.run(data, address, verbose)

def startServer():
    port = 12345
    ip = '0.0.0.0'
    verbose = '-v' in sys.argv
    
    data_manager.run()
    server = PortManager(ip, port, verbose, BUFFER_SIZE)
    
    print(f"[S] server inicializado e operando de forma assíncrona na porta {port}.")
    server.listenPort(lambda data, address: processData(data, address, verbose))
    if verbose:
        print("\n[V] Modo de depuração ativo.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.closeConnections()
        print("\n[S] Processo do server encerrado pelo operador.")

if __name__ == "__main__":
    startServer()