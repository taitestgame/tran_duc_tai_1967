import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_Form   # nếu file bạn là Ui_Form thì giữ nguyên


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # connect button
        self.ui.pushButton_Encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_Decrypt.clicked.connect(self.call_api_decrypt)

    # ===== ENCRYPT =====
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"

        payload = {
            "plain_text": self.ui.text_plain_text.toPlainText(),
            "key": self.ui.text_key.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                self.ui.text_cipher_text.setPlainText(
                    data["encrypted_message"]
                )

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()

            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    # ===== DECRYPT =====
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"

        payload = {
            "cipher_text": self.ui.text_cipher_text.toPlainText(),
            "key": self.ui.text_key.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                self.ui.text_plain_text.setPlainText(
                    data["decrypted_message"]
                )

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()

            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())