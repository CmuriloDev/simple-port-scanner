import socket #para conversar com a placa de rede
from datetime import datetime 
import sys 
import concurrent.futures

#Função para ser executada por cada thread
def scan_port(ip_alvo, porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        resultado = s.connect_ex((ip_alvo, porta))
        s.close()
        
        if resultado == 0:
            print(f"[+] Porta {porta} está ABERTA")

    except:
        pass

    return None
        

def run_scanner():
    print("-" * 60)
    print("PYTHON PORT SCANNER")
    print("-" * 60)

    alvo = input("Digite o IP ou o URL do seu alvo (ex: scanme.nmap.org): ").strip()

# Remover http:// ou https:// do alvo, se presente
    if alvo.startswith("http://"):
        alvo = alvo.replace("http://", "")
    elif alvo.startswith("https://"):
        alvo = alvo.replace("https://", "")

# Obter o endereço IP do alvo
    try:
        porta_inicial = int(input("Digite a porta inicial: "))
        porta_final = int(input("Digite a porta final: "))
    except ValueError:
        print("\n[!] Erro: As portas devem ser números inteiros.")
        sys.exit()

#Validar o intervalo de portas
    if porta_inicial < 0 or porta_final > 65535 or porta_inicial > porta_final:
        print("\n[!] Erro: Intervalo de portas inválido. Use 0-65535.")
        sys.exit()

    try:
        ip_alvo = socket.gethostbyname(alvo)
    except socket.gaierror:
        print(f"\n[!] Erro: Não foi possível resolver o nome '{alvo}'. Verifique a digitação e tente novamente.")
        sys.exit()

# Inicia o Scan
    print("\n" + "-" * 60)
    print(f"Iniciando Scan no alvo: {alvo} ({ip_alvo})")
    print(f"Intervalo de Portas: {porta_inicial} até {porta_final}")
    print(f"Threads simultâneas: 50")
    print(f"Horário de início: {datetime.now()}")
    print("-" * 60)

    inicio_tempo = datetime.now()

    try:
        # ThreadPoolExecutor gerencia as threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            for porta in range(porta_inicial, porta_final + 1):
                executor.submit(scan_port, ip_alvo, porta)

    except KeyboardInterrupt:
        print("\n\n[!] Scan interrompido pelo usuário (Ctrl+C).")
        sys.exit()
    except socket.error:   
        print("\n[!] Erro de conexão com o servidor.")
        sys.exit()

    fim_tempo = datetime.now()
    duracao = fim_tempo - inicio_tempo

    print("-" * 60)
    print(f"Scan finalizado com sucesso em {duracao}.")

if __name__ == "__main__":
    run_scanner()
    









