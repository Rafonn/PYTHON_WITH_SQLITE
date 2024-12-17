import json
import time
from filtragem import JsonManager
from db import DatabaseManager

# Para gerar executável (necessário pyinstaller): 'pyinstaller --onefile main.py'.

def leitura_filtragem(caminho_json, caminho_saida): # Executar a leitura e a filtragem dos dados da global.json.
    json_manager = JsonManager(caminho_json, caminho_saida)
    json_manager.executar()

def db_send(caminho_json, db_name): # Executar o envio para o banco de dados.
    with open(caminho_json, 'r', encoding='utf-8') as arquivo:
        dados_json = json.load(arquivo)

    db_manager = DatabaseManager(db_name)

    for loom, dados in dados_json.items():
        db_manager.criar_tabela(loom, dados)
        db_manager.inserir_dados(loom, dados)

    db_manager.salvar()
    db_manager.fechar()

def executar(caminho_json, caminho_saida, db_name): # Função Main (chama as outras duas na ordem correta)
    print('Executando...')
    leitura_filtragem(caminho_json, caminho_saida)
    db_send(caminho_saida, db_name)

caminho_json = r'C:\Users\Industria 4.0\.node-red\context\global\global.json' # Caminho para a pasta de globais.
caminho_saida = 'dados_salvos.json' # Caminho para os dados de saída da filtragem.
db_name = 'C:\\Users\\Industria 4.0\\Desktop\\Bases de dados\\dadosNodeRed.db' # Caminho para a base de dados.

while True:
    try:
        executar(caminho_json, caminho_saida, db_name)
        time.sleep(300)  # Espera 300 segundos (5 minutos)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        time.sleep(10)  # Espera 10 segundos antes de tentar novamente após o erro