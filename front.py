import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer # QTimer é opcional se o JS já faz o setInterval

class AeroGuardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AeroGuard - Monitor de Tráfego Aéreo")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.browser = QWebEngineView()
        
        # --- ESTA É A LINHA MAIS IMPORTANTE PARA CORRIGIR O SEU ERRO ---
        # 1. Altere para a URL do seu servidor Flask
        # 2. Certifique-se que o Flask está rodando e servindo o HTML nesta URL
        self.browser.setUrl(QUrl("http://127.0.0.1:5000/")) # Carrega a rota raiz do seu Flask
        
        layout.addWidget(self.browser)

        # Se você quiser adicionar elementos PyQt ao lado do mapa, faria aqui
        # Ex: QPushButton("Botão")
        # layout.addWidget(QPushButton("Botão de Teste"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AeroGuardWindow()
    window.showMaximized()
    sys.exit(app.exec_())