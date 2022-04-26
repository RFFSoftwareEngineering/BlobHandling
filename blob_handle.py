import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sqlite3
import mysql.connector as mc
import keyring


class MainTree(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Teste Blob")
        self.showMaximized()
        self.setStyleSheet("background-color: #e9f2f0")

        self.label_blob = QLabel("", self)
        self.label_blob.move(570, 150)
        self.label_blob.show()

        self.btn_teste = QPushButton("Salvar Blob", self)
        self.btn_teste.move(720, 550)
        self.btn_teste.show()
        self.btn_teste.clicked.connect(self.BlobSave)

        service_id = 'xxxxx'
        keyring.set_password(service_id, None, 'xxxxxxx')

        try:
            password_key = keyring.get_password(service_id, None)
            con = mc.connect(
                host="xxxxxxxxx",
                user="xxxxxxxxx",
                password=password_key,
                database="xxxxxxxx"
            )
            
            query = f"""
                    CREATE TABLE IF NOT EXISTS knowhow.cadastro_clientes_fornecedores_icons (
                    ID integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
                    Image MEDIUMBLOB,
                    PersonID int REFERENCES knowhow.cadastro_clientes_fornecedores (PersonID)
                    );
                    """
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            cursor.close()
            con.close()         
            
            msg = QMessageBox()
            msg.setText("Table de Imagens Criada Com Sucesso")
            msg.setWindowTitle("Create Table")
            msg.exec()
        except mc.Error as e:
            msg = QMessageBox()
            msg.setText(f"Falha ao Conectar ao Banco de Dados:{e}")
            msg.setWindowTitle("Connection")
            msg.exec()
            sys.exit(1)

        self.btn_get = QPushButton("Get Blob", self)
        self.btn_get.move(720, 650)
        self.btn_get.show()
        self.btn_get.clicked.connect(self.retrive_blob)


    def write_to_file(self, file_name, binary_data):
        with open(file_name, "wb") as file:
            file.write(binary_data)
        print("[DATA] : The following file has been written to the project directory: ", file_name)


    def convert_into_binary(self, file_path):
        with open(file_path, 'rb') as file:
          photo_image = file.read()
        return photo_image


    def retrive_blob(self):
        service_id = 'xxxxxxx'
        keyring.set_password(service_id, None, 'xxxxxxxx')

        try:
            password_key = keyring.get_password(service_id, None)
            con = mc.connect(
                host="xxxxxxxx",
                user="xxxxxxxx",
                password=password_key,
                database="xxxxxxxx"
            )
            query = """
                      SELECT * FROM knowhow.cadastro_clientes_fornecedores_icons;
                    """
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            con.commit()
            cursor.close()
            con.close() 
            print(result)

        except mc.Error as e:
            msg = QMessageBox()
            msg.setText(f"Falha :{e}")
            msg.setWindowTitle("Connection")
            msg.exec()

        x = 0
        
        for row in result:
            x = row[0]
            file_path = f'C:/LogosCadastroClientes/CadNumber{x}.jpg'
            file_bin = row[1]
            self.write_to_file(file_path, file_bin) # FAZER PREVIOUS E NEXT 

        self.pic_pixmap = QPixmap(file_path)
        self.pic_pixmap = self.pic_pixmap.scaledToWidth(350)


        self.label_blob.setPixmap(self.pic_pixmap)
        self.label_blob.resize(350, 350)

        msg = QMessageBox()
        msg.setText("Dados escritos no diretorio do projeto com sucesso!")
        msg.setWindowTitle("Success!")
        msg.exec()


    def BlobSave(self):
        self.fname = QFileDialog.getOpenFileName(self, "Open File", "C:\\", "Image Files (*.jpg *.png)")
        self.fnamepath = self.fname[0]
        print(self.fnamepath)

        self.file_blob = self.convert_into_binary(self.fnamepath)

        print("converteu")

        service_id = 'xxxxxxx'
        keyring.set_password(service_id, None, '-Know-!-How-')

        try:
            password_key = keyring.get_password(service_id, None)
            con = mc.connect(
                host="xxxxxxxxx",
                user="xxxxxxxxx",
                password=password_key,
                database="xxxxxxxx"
            )
            query = """
                        INSERT INTO knowhow.cadastro_clientes_fornecedores_icons VALUES (%s, %s, %s)
                    """

            cursor = con.cursor()
            cursor.execute(query, (None, self.file_blob, 3)) # colocar variável com o valor do id do cliente
            con.commit()
            cursor.close()
            con.close()

            self.pic_pixmap = QPixmap(self.fnamepath)
            self.pic_pixmap = self.pic_pixmap.scaledToWidth(350)


            self.label_blob.setPixmap(self.pic_pixmap)
            self.label_blob.resize(350, 350)


            msg = QMessageBox()
            msg.setText("Imagem salva com sucesso!")
            msg.setWindowTitle("Img Status")
            msg.exec()

        except mc.Error as e:
            msg = QMessageBox()
            msg.setText(f"Falha :{e}")
            msg.setWindowTitle("Connection")
            print(e)
            msg.exec()


app = QApplication(sys.argv)

teste_blob = MainTree()
teste_blob.show()
app.exec()

