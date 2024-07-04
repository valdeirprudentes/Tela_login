from PyQt5 import  uic,QtWidgets, QtGui, QtCore
import pyodbc

# Configurações de conexão com o SQL Server
server = 'VALDEIR' 
database = 'cadastro' 
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'


def chama_segunda_tela():
    primeira_tela.label_6.setText("")
    nome_usuario = primeira_tela.lineEdit.text()
    senha = primeira_tela.lineEdit_2.text()

    # Verifica se o usuário está embutido no código
    if nome_usuario == "joao123" and senha == "123456" :
        primeira_tela.close()
        segunda_tela.show()
        return
    
    elif nome_usuario == "val" and senha == "123" :
        primeira_tela.close()
        segunda_tela.show()
        return
    
    # Verifica se o usuário está no banco de dados
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cadastro WHERE login = ? AND senha = ?", (nome_usuario, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            primeira_tela.close()
            segunda_tela.show()

        else :
            primeira_tela.label_6.setText("Dados de login incorretos!")    
    except pyodbc.Error as erro:
        primeira_tela.label_6.setText("Erro ao verificar os dados de login")
        print("Erro ao verificar os dados de login: ", erro)

def logout():
    segunda_tela.close()
    primeira_tela.show() 

def abre_tela_cadastro():
    tela_cadastro.show()

def cadastrar():
    nome = tela_cadastro.lineEdit.text()
    login = tela_cadastro.lineEdit_2.text()
    senha = tela_cadastro.lineEdit_3.text()
    c_senha = tela_cadastro.lineEdit_4.text()

    # Preenchimento obrigatório de todos os campos no cadastro
    if not nome or not login or not senha or not c_senha:
        tela_cadastro.label.setText("Todos os campos são obrigatórios")
        return

    if (senha == c_senha):
        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            cursor.execute("IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='cadastro' AND xtype='U')"
                           " CREATE TABLE cadastro (nome NVARCHAR(100), login NVARCHAR(100), senha NVARCHAR(100))")
            cursor.execute("INSERT INTO cadastro (nome, login, senha) VALUES (?, ?, ?)", (nome, login, senha))

            conn.commit()            
            tela_cadastro.label.setText("Usuario cadastrado com sucesso")

        except pyodbc.Error as erro:
            tela_cadastro.label.setText("Erro ao inserir os dados: " + str(erro))
            print("Erro ao inserir os dados: ",erro)

        
        finally:
            conn.close()
    else:
        tela_cadastro.label.setText("As senhas digitadas estão diferentes")
      

app=QtWidgets.QApplication([])
primeira_tela=uic.loadUi("primeira_tela.ui")
segunda_tela = uic.loadUi("segunda_tela.ui")
tela_cadastro = uic.loadUi("tela_cadastro.ui")

primeira_tela.pushButton.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(logout)
primeira_tela.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
primeira_tela.pushButton_2.clicked.connect(abre_tela_cadastro)
tela_cadastro.pushButton.clicked.connect(cadastrar) 

# Mudando o cursor para o botão LOGIN
primeira_tela.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

# Mudando o cursor para o botão CADASTRE-SE
primeira_tela.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

# Mudando o cursor para o botão LOGOUT
segunda_tela.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

# Mudando o cursor para o botão CADASTRAR
tela_cadastro.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

primeira_tela.show()
app.exec()