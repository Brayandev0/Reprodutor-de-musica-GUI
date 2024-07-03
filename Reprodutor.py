from PySide6.QtWidgets import QApplication,QWidget, QMessageBox,QTableWidgetItem
from click import clear
from tt import Ui_Form
import sys
import base64
import requests

class my_app(QWidget):
    def __init__(self) :
        super().__init__()
        self.page = Ui_Form()
        self.page.setupUi(self)
        self.token_acesso = self.pegar_token()
        self.page.botao_pesquisar_musica.clicked.connect(lambda: self.validar_musica())
        self.setWindowTitle("Music replay")
    #   Função para verificar se a musica é válida 
    def validar_musica(self):
        texto = self.page.tela_de_pesquisa_musicas.text()
        if len(texto) < 3 or not texto:
            self.logs_de_erro("Música invalída ")
            return False
        self.buscar_musicas(texto)
    #   Tela de erro 
    def logs_de_erro(self,valor: str):
        erro = QMessageBox()
        erro.setText(valor)
        erro.setWindowTitle("Erro")
        erro.setIcon(QMessageBox().Icon.Critical)
        erro.exec()
    #   Função para realizar a requisição de pesquisa 
    def buscar_musicas(self,consulta):
        url_De_pesquisa = 'https://api.spotify.com/v1/search'
        search_params = {
        'q': consulta,
        'type': 'track',
        'market': 'BR',
        'limit': 7,
        'include_external': 'audio'
    }
        headers = {
            'Authorization': f'Bearer {self.token_acesso}'
        }

        requisicao = requests.get(url_De_pesquisa,headers=headers,params=search_params)
        for i in range(0,7):       
            nome_da_musica = requisicao.json()['tracks']['items'][i]['name']
            id_da_musica = requisicao.json()['tracks']['items'][i]['id']
            nome = requisicao.json()['tracks']['items'][i]['album']['artists'][0]['name']
            linha = self.page.tableWidget.rowCount()
            self.page.tableWidget.insertRow(linha)
            nome_musica_final = QTableWidgetItem(nome_da_musica)
            id_da_musica = QTableWidgetItem(id_da_musica)
            nome = QTableWidgetItem(nome)
            self.page.tableWidget.setItem(linha,0,nome_musica_final)
            self.page.tableWidget.setItem(linha,2,id_da_musica)
            self.page.tableWidget.setItem(linha,1,nome)


     #  Função para pegar o Token de autenticação        
    def pegar_token(self):
        client_id = Secret 
        secret = Secret
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_header = base64.b64encode((client_id + ':' + secret).encode()).decode('utf-8')
        auth_data = {'grant_type': 'client_credentials'}

        response = requests.post(auth_url, headers={'Authorization': 'Basic ' + auth_header}, data=auth_data)
        if response.status_code == 200:
            final = response.json()
            return final['access_token']
           
        else:
            print(response.json())
            print("sdwed")
            raise Exception('Failed to obtain access token')
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = my_app()
    janela.show()
    app.exec()
