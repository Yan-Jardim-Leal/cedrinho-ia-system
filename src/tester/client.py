from port_manager import PortManager

def inicializar_transmissor():
    print("[S] Módulo transmissor ativado.")
    entrada_porta = input("[Port] ")
    
    try:
        porta_alvo = int(entrada_porta)
    except ValueError:
        print("[ERRO FATAL] O valor da porta deve ser do tipo numérico (inteiro). Operação abortada.")
        return
        
    while True:
        carga_dados = input("[T] ")
        cliente = PortManager('127.0.0.1', porta_alvo)
        
        try:
            resposta_bruta = cliente.callPort(carga_dados)
            resposta_processada = resposta_bruta.decode('utf-8')
            print(f"[R] {resposta_processada}")
            
        except KeyboardInterrupt:
            cliente.closeConnections()
            print("\n[S] Processo do servidor encerrado pelo operador.")
        except ConnectionRefusedError:
            print(f"[*] Conexão recusada na porta {porta_alvo}. Verifique se o Módulo 1 (Servidor) está ativo.")
        except Exception as erro_geral:
            print(f"[*] {erro_geral}")

if __name__ == "__main__":
    inicializar_transmissor()