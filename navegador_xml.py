import sys
import os
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QLineEdit,
    QTabWidget, QFileDialog, QMessageBox, QDialog,
    QListWidget, QVBoxLayout, QPushButton, QInputDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


# =========================
# Funções XML
# =========================
def init_xml(path, filename, root_name):
    file = os.path.join(path, filename)
    if not os.path.exists(file):
        root = ET.Element(root_name)
        tree = ET.ElementTree(root)
        tree.write(file, encoding="utf-8", xml_declaration=True)


def add_xml_entry(path, filename, tag, text):
    file = os.path.join(path, filename)
    tree = ET.parse(file)
    root = tree.getroot()
    entry = ET.SubElement(root, tag)
    entry.text = text
    tree.write(file, encoding="utf-8", xml_declaration=True)


def read_xml_entries(path, filename):
    file = os.path.join(path, filename)
    tree = ET.parse(file)
    return [e.text for e in tree.getroot() if e.text]


def clear_xml(path, filename, root_name):
    root = ET.Element(root_name)
    tree = ET.ElementTree(root)
    tree.write(os.path.join(path, filename),
               encoding="utf-8",
               xml_declaration=True)


# =========================
# Gestor de Favoritos
# =========================
class FavoritesManager(QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.setWindowTitle("Favoritos (XML)")
        self.resize(300, 400)

        layout = QVBoxLayout(self)
        self.list = QListWidget()
        layout.addWidget(self.list)

        btn_open = QPushButton("Abrir")
        btn_open.clicked.connect(self.accept)
        layout.addWidget(btn_open)

        self.load()

    def load(self):
        self.list.clear()
        for url in read_xml_entries(self.path, "favorites.xml"):
            self.list.addItem(url)


# =========================
# Gestor de Histórico
# =========================
class HistoryManager(QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.setWindowTitle("Histórico (XML)")
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
        for url in read_xml_entries(self.path, "history.xml"):
            self.list.addItem(url)

    def clear(self):
        clear_xml(self.path, "history.xml", "history")
        self.load()


# =========================
# Navegador Principal
# =========================
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador PyQt5 (XML)")
        self.resize(1200, 800)

        # Pasta de dados
        self.data_path = os.getcwd()

        # Inicializar XML
        init_xml(self.data_path, "favorites.xml", "favorites")
        init_xml(self.data_path, "history.xml", "history")

        # Abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url)
        self.setCentralWidget(self.tabs)

        # Barra
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.go_url)

        self.add_btn("◀", lambda: self.current().back())
        self.add_btn("▶", lambda: self.current().forward())
        self.add_btn("⟳", lambda: self.current().reload())
        self.navbar.addWidget(self.url_bar)

        self.add_btn("Abrir", self.open_file)
        self.add_btn("Abrir URL", self.open_url_dialog)
        self.add_btn("Guardar link", self.add_favorite)
        self.add_btn("Guardar onde", self.choose_folder)
        self.add_btn("Sair", QApplication.quit)

        self.create_menu()
        self.new_tab(QUrl("https://www.google.com"), "Início")

    # ---------- Utilitários ----------
    def add_btn(self, text, func):
        act = QAction(text, self)
        act.triggered.connect(func)
        self.navbar.addAction(act)

    def current(self):
        return self.tabs.currentWidget()

    # ---------- Abas ----------
    def new_tab(self, url, title):
        view = QWebEngineView()
        view.setUrl(url)
        i = self.tabs.addTab(view, title)
        self.tabs.setCurrentIndex(i)

        view.urlChanged.connect(self.record_history)
        view.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()))
        view.loadFinished.connect(lambda: self.tabs.setTabText(i, view.title()))

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
        file_menu = self.menuBar().addMenu("Ficheiro")
        file_menu.addAction("Abrir ficheiro", self.open_file)
        file_menu.addAction("Abrir URL", self.open_url_dialog)
        file_menu.addAction("Guardar link", self.add_favorite)
        file_menu.addAction("Guardar onde", self.choose_folder)
        file_menu.addSeparator()
        file_menu.addAction("Sair", QApplication.quit)

        view_menu = self.menuBar().addMenu("Ver")
        view_menu.addAction("Favoritos", self.show_favorites)
        view_menu.addAction("Histórico", self.show_history)

    # ---------- Funcionalidades ----------
    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Abrir ficheiro", "", "HTML (*.html *.htm)"
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
            init_xml(folder, "favorites.xml", "favorites")
            init_xml(folder, "history.xml", "history")
            QMessageBox.information(self, "Pasta definida", folder)

    def add_favorite(self):
        add_xml_entry(self.data_path, "favorites.xml",
                      "url", self.current().url().toString())
        QMessageBox.information(self, "Favoritos", "Link guardado em XML")

    def record_history(self, url):
        add_xml_entry(self.data_path, "history.xml", "url", url.toString())

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
