import serial
import requests
import time
import sys # Usado para sair do script se o login falhar

# --- Seção de Configuração ---
PORTA_SERIAL = 'COM10' # Mude se necessário
URL_BASE = "http://20.201.78.232:8080"
URL_LOGIN = f"{URL_BASE}/login" # SEU ENDPOINT DE LOGIN
URL_ATUALIZACAO = f"{URL_BASE}/insight/vincular-ala"

# Suas credenciais para obter o token
USUARIO = "gabrielly.cmacedo@gmail.com" # O usuário que seu backend espera
SENHA = "senhaSegura123" # A senha que seu backend espera
# --- Fim da Configuração ---


def obter_token(url_login, usuario, senha):
    """Função para autenticar e obter o token JWT."""
    print(f"Tentando autenticar no endpoint: {url_login}")
    try:
        payload_login = {
            "email": usuario, # Ajuste as chaves se seu DTO de login for diferente
            "password": senha
        }
        response = requests.post(url_login, json=payload_login)

        if response.status_code == 200:
            # Supondo que o token venha num campo 'token' no JSON de resposta
            token = response.json().get('token') 
            if token:
                print("Autenticação bem-sucedida. Token recebido!")
                return token
            else:
                print("Erro: Resposta OK, mas o campo 'token' não foi encontrado no JSON.")
                return None
        else:
            print(f"Falha na autenticação. Status: {response.status_code}, Resposta: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão durante a autenticação: {e}")
        return None

# --- Início da Execução Principal ---

# 1. Obter o token
token_jwt = obter_token(URL_LOGIN, USUARIO, SENHA)

if not token_jwt:
    print("Não foi possível obter o token de autenticação. Encerrando o script.")
    sys.exit() # Encerra o programa se não conseguir logar

# 2. Conectar ao Arduino (só depois de ter o token)
try:
    arduino = serial.Serial(PORTA_SERIAL, 9600, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"Erro ao conectar na porta serial: {e}")
    sys.exit()

# 3. Loop Principal para ler dados e enviar atualizações
print("\nPonte de comunicação iniciada. Aguardando dados do Arduino...")
while True:
    try:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            # ... (a lógica de validação da linha continua a mesma) ...
            if ',' in line:
                try:
                    parts = line.split(',')
                    moto_id = int(parts[0].strip())
                    ala_id = int(parts[1].strip())

                    payload_atualizacao = { "motoId": moto_id, "alaId": ala_id }
                    
                    # --- MONTAGEM DO CABEÇALHO DE AUTORIZAÇÃO ---
                    headers = {
                        'Authorization': f'Bearer {token_jwt}'
                    }
                    
                    print(f"Enviando para o backend: {payload_atualizacao}")
                    response = requests.post(
                        URL_ATUALIZACAO, 
                        json=payload_atualizacao,
                        headers=headers # Envia o cabeçalho com o token
                    )
                    print(f"Resposta do backend: {response.status_code}")

                except ValueError:
                    # Ignora linhas que não são dados numéricos
                    pass
            
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro de conexão: {e}")
        time.sleep(5) 
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
        break

arduino.close()