import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from ui.chat1 import Ui_MainWindow 

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

class ServerThread(QThread):
    msg_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    
    # Gửi AES key ra ngoài cho UI dùng để mã hóa khi gửi
    key_ready_signal = pyqtSignal(bytes, object) 

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', 12345))
        self.server.listen(1)
        self.status_signal.emit("Hệ thống: Đang chờ User 2 kết nối...")

        self.conn, addr = self.server.accept()
        self.status_signal.emit("Hệ thống: User 2 đã kết nối. Đang trao đổi khóa...")

        try:
            # Logic trao đổi key y hệt file server.py của bạn
            server_key = RSA.generate(2048)
            self.conn.send(server_key.publickey().export_key(format='PEM'))
            
            client_received_key = RSA.import_key(self.conn.recv(2048))
            
            aes_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(client_received_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            self.conn.send(encrypted_aes_key)
            
            self.status_signal.emit("Hệ thống: Bắt tay thành công. Sẵn sàng chat an toàn.")
            self.key_ready_signal.emit(aes_key, self.conn)

            # Vòng lặp nhận tin nhắn
            while True:
                encrypted_message = self.conn.recv(1024)
                if not encrypted_message: break
                
                decrypted_message = decrypt_message(aes_key, encrypted_message)
                self.msg_signal.emit(f"User 2: {decrypted_message}")
                
        except Exception as e:
            self.status_signal.emit(f"Lỗi: {e}")

class User1App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.aes_key = None
        self.conn = None

        self.ui.btn_send1.clicked.connect(self.send_message)

        self.worker = ServerThread()
        self.worker.msg_signal.connect(self.display_msg)
        self.worker.status_signal.connect(self.display_msg)
        self.worker.key_ready_signal.connect(self.set_network_data)
        self.worker.start()

    def set_network_data(self, aes_key, conn):
        self.aes_key = aes_key
        self.conn = conn

    def send_message(self):
        try:
            msg = self.ui.txt_input1.toPlainText().strip()
        except AttributeError:
            msg = self.ui.txt_input1.text().strip()

        if msg and self.conn and self.aes_key:
            try:
                # Dùng hàm mã hóa của bạn
                enc_msg = encrypt_message(self.aes_key, msg)
                self.conn.send(enc_msg)
                
                self.display_msg(f"User 1: {msg}")
                self.ui.txt_input1.clear()
            except Exception as e:
                self.display_msg(f"Lỗi gửi tin: {e}")

    def display_msg(self, text):
        self.ui.txt_chat1.appendPlainText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = User1App()
    window.show()
    sys.exit(app.exec_())