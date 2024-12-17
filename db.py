import json
import sqlite3
import os
from datetime import datetime

#db_name = 'C:\\Users\\Industria 4.0\\Desktop\\Bases de dados\\dadosNodeRed.db'

class DatabaseManager:
    def __init__(self, db_name):
        self.conexao = sqlite3.connect(db_name)
        self.cursor = self.conexao.cursor()
    
    def obter_esquema_tabela(self, loom):
        query = f"PRAGMA table_info({loom})"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def excluir_tabela(self, loom): # (NÃO CHAME!) Usar APENAS caso queira deletar uma tabela existente.
        query = f"DROP TABLE IF EXISTS {loom}"
        self.cursor.execute(query)

    def criar_tabela(self, loom, dados):
        if not dados:
            print(f"Nenhum dado encontrado para {loom}. Não será criada uma tabela.")
            return

        colunas_existentes = {col[1] for col in self.obter_esquema_tabela(loom)}
        
        colunas = []
        for chave, valor in dados.items():
            if chave not in colunas_existentes:
                colunas.append(f"{chave} {self.definir_tipo(valor)}")
        
        if colunas:
            colunas = ', '.join(colunas)
            colunas += ', created_at TEXT'
            query = f"CREATE TABLE IF NOT EXISTS {loom} (id INTEGER PRIMARY KEY AUTOINCREMENT, {colunas})"
            print(f"Executando query para criar tabela: {query}")
            self.cursor.execute(query)

        try:
            for chave in dados.keys():
                if chave not in colunas_existentes:
                    self.cursor.execute(f"ALTER TABLE {loom} ADD COLUMN {chave} {self.definir_tipo(dados[chave])}")
        except sqlite3.OperationalError:
            pass

    def definir_tipo(self, valor):
        if isinstance(valor, int):
            return 'INTEGER'
        elif isinstance(valor, float):
            return 'REAL'
        elif isinstance(valor, str):
            return 'TEXT'
        elif isinstance(valor, bool):
            return 'BOOLEAN'
        else:
            return 'TEXT'

    def inserir_dados(self, loom, dados):
        if not dados:
            print(f"Nenhum dado para inserir em {loom}.")
            return
        
        colunas = ', '.join(dados.keys()) + ', created_at'
        marcadores = ', '.join(['?' for _ in dados] + ['?'])
        query = f"INSERT INTO {loom} ({colunas}) VALUES ({marcadores})"
        dados['created_at'] = datetime.now().isoformat()
        self.cursor.execute(query, tuple(dados.values()))

    def salvar(self):
        self.conexao.commit()

    def fechar(self):
        self.conexao.close()

def main():
    caminho_json = 'dados_salvos.json'
    with open(caminho_json, 'r', encoding='utf-8') as arquivo:
        dados_json = json.load(arquivo)

    db_name = 'C:\\Users\\Industria 4.0\\Desktop\\Bases de dados\\dadosNodeRed.db'
    db_manager = DatabaseManager(db_name)

    for loom, dados in dados_json.items():
        db_manager.criar_tabela(loom, dados)
        db_manager.inserir_dados(loom, dados)

    db_manager.salvar()
    db_manager.fechar()