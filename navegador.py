import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QLineEdit,
    QTabWidget, QFileDialog, QMessageBox, QDialog,
    QListWidget, QVBoxLayout, QPushButton, QInputDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


# =========================
# Gestor de Favoritos
# =========================
class FavoritesManager(QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.setWindowTitle("Favoritos")
        self.resize(300, 400)

        layout = QVBoxLayout(self)
        self.list = QListWidget()
        layout.addWidget(self.list)

        btn_open = QPushButton("Abrir")
        btn_open.clicked.connect(self.accept)
        layout.addWidget(btn_open)

        btn_remove = QPushButton("Remover")
        btn_remove.clicked.connect(self.remove_item)
        layout.addWidget(btn_remove)

        self.load()

    def load(self):
        self.list.clear()
        file = os.path.join(self.path, "favorites.txt")
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    self.list.addItem(line.strip())

    def remove_item(self):
        item = self.list.currentItem()
        if not item:
            return
        file = os.path.join(self.path, "favorites.txt")
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(file, "w", encoding="utf-8") as f:
            for l in lines:
                if l.strip() != item.text():
                    f.write(l)
        self.load()


# =========================
# Gestor de Histórico
# =========================
class HistoryManager(QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.setWindowTitle("Histórico")
        self.resize(300, 400)

        layout = QVBoxLayout(self)
        self.list = QListWidget()
        layout.addWidget(self.list)

        btn_open = QPushButton("Abrir")
        btn_open.clicked.connect(self.accept)
        layout.addWidget(btn_open)

        btn_clear = QPushButton("Limpar")
        btn_clear.clicked.connect(self.clear)
        layout.addWidget(btn_clear)

        self.load()

    def load(self):
        self.list.clear()
        file = os.path.join(self.path, "history.txt")
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    self.list.addItem(line.strip())

    def clear(self):
        open(os.path.join(self.path, "history.txt"), "w").close()
        self.load()


# =========================
# Navegador Principal
# =========================
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador PyQt5")
        self.resize(1200, 800)

        # Pasta onde tudo é guardado
        self.data_path = os.getcwd()

        # Abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url)
        self.setCentralWidget(self.tabs)

        # Barra de navegação
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.go_url)

        # Botões
        self.add_button("◀", lambda: self.current().back())
        self.add_button("▶", lambda: self.current().forward())
        self.add_button("⟳", lambda: self.current().reload())
        self.navbar.addWidget(self.url_bar)

        self.add_button("Abrir", self.open_file)
        self.add_button("Abrir URL", self.open_url_dialog)
        self.add_button("Guardar link", self.add_favorite)
        self.add_button("Guardar onde", self.choose_folder)
        self.add_button("Sair", QApplication.quit)

        # Menu
        self.create_menu()

        # Aba inicial
        self.new_tab(QUrl("https://www.google.com"), "Início")

    # ---------- Utilitários ----------
    def add_button(self, text, func):
        action = QAction(text, self)
        action.triggered.connect(func)
        self.navbar.addAction(action)

    def current(self):
        return self.tabs.currentWidget()

    # ---------- Abas ----------
    def new_tab(self, url, title):
        browser = QWebEngineView()
        browser.setUrl(url)
        i = self.tabs.addTab(browser, title)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(self.record_history)
        browser.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()))
        browser.loadFinished.connect(lambda: self.tabs.setTabText(i, browser.title()))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    # ---------- Navegação ----------
    def go_url(self):
        self.current().setUrl(QUrl(self.url_bar.text()))

    def update_url(self):
        if self.current():
            self.url_bar.setText(self.current().url().toString())

    # ---------- Menu ----------
    def create_menu(self):
        menu = self.menuBar().addMenu("Ficheiro")

        menu.addAction("Abrir ficheiro", self.open_file)
        menu.addAction("Abrir URL", self.open_url_dialog)
        menu.addAction("Guardar link", self.add_favorite)
        menu.addAction("Guardar onde", self.choose_folder)
        menu.addSeparator()
        menu.addAction("Sair", QApplication.quit)

        menu2 = self.menuBar().addMenu("Ver")
        menu2.addAction("Favoritos", self.show_favorites)
        menu2.addAction("Histórico", self.show_history)

    # ---------- Funcionalidades ----------
    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Abrir ficheiro", "", "HTML (*.html *.htm);;Todos (*.*)"
        )
        if file:
            self.current().setUrl(QUrl.fromLocalFile(file))

    def open_url_dialog(self):
        url, ok = QInputDialog.getText(self, "Abrir URL", "Endereço:")
        if ok and url:
            self.current().setUrl(QUrl(url))

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher pasta")
        if folder:
            self.data_path = folder
            QMessageBox.information(self, "Pasta", folder)

    def add_favorite(self):
        file = os.path.join(self.data_path, "favorites.txt")
        with open(file, "a", encoding="utf-8") as f:
            f.write(self.current().url().toString() + "\n")
        QMessageBox.information(self, "Favoritos", "Link guardado")

    def record_history(self, url):
        file = os.path.join(self.data_path, "history.txt")
        with open(file, "a", encoding="utf-8") as f:
            f.write(url.toString() + "\n")

    def show_favorites(self):
        dlg = FavoritesManager(self.data_path, self)
        if dlg.exec_():
            item = dlg.list.currentItem()
            if item:
                self.current().setUrl(QUrl(item.text()))

    def show_history(self):
        dlg = HistoryManager(self.data_path, self)
        if dlg.exec_():
            item = dlg.list.currentItem()
            if item:
                self.current().setUrl(QUrl(item.text()))


# =========================
# Arranque
# =========================
app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())
