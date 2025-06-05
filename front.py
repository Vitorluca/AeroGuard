import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer

class AeroGuardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AeroGuard - Monitor de Tráfego Aéreo")
        self.setGeometry(100, 100, 1200, 800) # x, y, width, height

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout vertical para o widget central
        layout = QVBoxLayout(central_widget)

        # Criar a visualização web
        self.browser = QWebEngineView()
        # Carrega o arquivo HTML local
        # Certifique-se de que 'map_display.html' está na mesma pasta que este script
        current_dir = sys.path[0] # Pega o diretório atual do script
        html_file_path = f"file:///{current_dir}/map_display.html"
        self.browser.setUrl(QUrl(html_file_path))
        
        layout.addWidget(self.browser)

        # Opcional: Você pode querer chamar uma função JS para atualizar os dados
        # a partir do Python, mas é mais comum deixar o JS fazer o fetch periodicamente.
        # Exemplo de como chamar JS do Python:
        # self.browser.page().runJavaScript("fetchAircraftData();")
        # Ou usando um QTimer para chamar periodicamente:
        # self.timer = QTimer(self)
        # self.timer.setInterval(5000) # 5 segundos
        # self.timer.timeout.connect(lambda: self.browser.page().runJavaScript("fetchAircraftData();"))
        # self.timer.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AeroGuardWindow()
    window.showMaximized() # Ou window.show() para tamanho definido
    sys.exit(app.exec_())