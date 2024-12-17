import json
import os

class JsonManager:
    def __init__(self, caminho_json, caminho_saida):
        self.caminho_json = caminho_json
        self.caminho_saida = caminho_saida

    def carregar_json(self):
        if not os.path.exists(self.caminho_json):
            print(f"Arquivo não encontrado: {self.caminho_json}")
            return None
        
        with open(self.caminho_json, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)

    def salvar_json(self, dados):
        with open(self.caminho_saida, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"Dados salvos em: {self.caminho_saida}")

    def agrupar_por_loom(self, dados):
        grupos = {f'loom{str(i).zfill(2)}': {} for i in range(1, 14)}

        for chave, valor in dados.items():
            if 'loom' in chave:
                numero_loom = chave.split('loom')[1][:2] 
                grupo_chave = f'loom{numero_loom.zfill(2)}'
                
                if grupo_chave in grupos:
                    grupos[grupo_chave][chave] = valor
        
        return grupos

    def coletar_informacoes(self):
        dados = self.carregar_json()
        if not dados:
            print("Nenhum dado para exibir.")
            return
        
        grupos = self.agrupar_por_loom(dados)

        self.salvar_json(grupos)

    def executar(self):
        self.coletar_informacoes()