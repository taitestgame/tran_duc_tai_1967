import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from ui.chat2 import Ui_MainWindow 

# Giữ nguyên hàm mã hóa của bạn
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

class ClientThread(QThread):
    msg_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    
    key_ready_signal = pyqtSignal(bytes, object)

    def run(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('localhost', 12345))
            self.status_signal.emit("Hệ thống: Đã kết nối với User 1. Đang trao đổi khóa...")

            # Logic trao đổi key y hệt file client.py của bạn
            client_key = RSA.generate(2048)
            server_public_key = RSA.import_key(self.client.recv(2048))
            
            self.client.send(client_key.publickey().export_key(format='PEM'))
            
            encrypted_aes_key = self.client.recv(2048)
            cipher_rsa = PKCS1_OAEP.new(client_key)
            aes_key = cipher_rsa.decrypt(encrypted_aes_key)
            
            self.status_signal.emit("Hệ thống: Bắt tay thành công. Sẵn sàng chat an toàn.")
            self.key_ready_signal.emit(aes_key, self.client)

            # Vòng lặp nhận tin nhắn
            while True:
                encrypted_message = self.client.recv(1024)
                if not encrypted_message: break
                
                decrypted_message = decrypt_message(aes_key, encrypted_message)
                self.msg_signal.emit(f"User 1: {decrypted_message}")
                
        except Exception as e:
            self.status_signal.emit(f"Lỗi: {e}")

class User2App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.aes_key = None
        self.client_socket = None

        # Đảm bảo tên biến pushButton và txt_input1 khớp với chat2.py
        self.ui.btn_send2.clicked.connect(self.send_message)

        self.worker = ClientThread()
        self.worker.msg_signal.connect(self.display_msg)
        self.worker.status_signal.connect(self.display_msg)
        self.worker.key_ready_signal.connect(self.set_network_data)
        self.worker.start()

    def set_network_data(self, aes_key, client_socket):
        self.aes_key = aes_key
        self.client_socket = client_socket

    def send_message(self):
        try:
            msg = self.ui.txt_input2.toPlainText().strip() 
        except AttributeError:
            msg = self.ui.txt_input2.text().strip()

        if msg and self.client_socket and self.aes_key:
            try:
                # Dùng hàm mã hóa của bạn
                enc_msg = encrypt_message(self.aes_key, msg)
                self.client_socket.send(enc_msg)
                
                self.display_msg(f"User 2: {msg}")
                self.ui.txt_input2.clear()
            except Exception as e:
                self.display_msg(f"Lỗi gửi tin: {e}")

    def display_msg(self, text):
        self.ui.txt_chat2.appendPlainText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = User2App()
    window.show()
    sys.exit(app.exec_())