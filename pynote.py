from PySide6 import QtCore
from PySide6.QtGui import QShortcut, QKeySequence, QIcon
from PySide6.QtWidgets import (QWidget, QApplication, QGridLayout, QPushButton, QListWidget, QTextEdit, QInputDialog,
                               QListWidgetItem)

from api_note import Note, get_notes


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyNote")
        self.resize(600, 400)

        self.setup_ui()
        self.loading_notes()

        icon_path = "./image/icon.png"
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)

    def setup_ui(self):
        self.create_layouts()
        self.create_widgets()
        self.modify()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_layouts(self):
        self.main_layout = QGridLayout(self)

    def create_widgets(self):
        self.btn_createNote = QPushButton("Create note")
        self.lw_notes = QListWidget()
        self.te_content = QTextEdit()

    def modify(self):
        # StyleSheet
        self.setStyleSheet(f"""
            background-color: rgb(255, 240, 167);
            """)

        self.btn_createNote.setStyleSheet(f"""
            QPushButton {{
                        background-color : rgb(255, 170, 81);
                
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: Coral;
                        
                        font-size: 18px;
                        font-weight: bold;
                    }}
            QPushButton:pressed {{
                                background-color: Coral;
                                border-style: inset;
                                border-width: 0px;
                            }}
            """)

        self.lw_notes.setStyleSheet(f"""
                QListWidget{{
                    background: rgb(255, 202, 149);
                    
                    border: 2px solid rgb(255, 170, 81);
                    border-radius: 10px;
                    padding: 1em;
                    
                    font-size: 16px;
                    font-weight: bold;
                    }}
                    
                QListWidget::item:hover {{
                    background: rgb(255, 170, 81);
                    border-radius: 10px;
                    }}
                    
                QListView::item:selected {{
                    color: black;
                    border : 2px solid rgb(255, 170, 81);
                    border-radius: 10px;
                    background : Coral;
                    }}
            """)

        self.te_content.setStyleSheet(f"""
                QTextEdit {{
                    background: rgb(255, 202, 149);
                    
                    border: 2px solid rgb(255, 170, 81);
                    border-radius: 10px;
                    padding: 1em;
                    
                    font-family: cursive;
                    font-size: 13px;
                    }}
            """)

        # Others
        self.te_content.setVisible(False)

    def add_widgets_to_layouts(self):
        # (y, x, h, l)
        self.main_layout.addWidget(self.btn_createNote, 0, 0, 1, 1)
        self.main_layout.addWidget(self.lw_notes, 1, 0, 1, 1)
        self.main_layout.addWidget(self.te_content, 0, 1, 2, 1)

    def setup_connections(self):
        self.btn_createNote.clicked.connect(self.create_note)
        self.te_content.textChanged.connect(self.save_note)
        self.lw_notes.itemSelectionChanged.connect(self.loading_note_content)
        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Delete), self.lw_notes, self.delete_selected_note)
        QShortcut(QKeySequence(QtCore.Qt.Key.Key_Backspace), self.lw_notes, self.delete_selected_note)

    ###############################################################
    def create_note(self):
        title, result = QInputDialog.getText(self, "Add a note", "Note title : ")
        if result and title:
            note = Note(title=title)
            note.save()
            self.add_note_to_listwidget(note)

    def delete_selected_note(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            result = selected_item.note.delete()
            if result:
                row = self.lw_notes.row(selected_item)
                self.lw_notes.takeItem(row)

    def loading_notes(self):
        notes = get_notes()
        for note in notes:
            self.add_note_to_listwidget(note)

    def loading_note_content(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            self.te_content.setVisible(True)
            self.te_content.setText(selected_item.note.content)
        else:
            self.te_content.setVisible(False)
            self.te_content.clear()

    def save_note(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            selected_item.note.content = self.te_content.toPlainText()
            selected_item.note.save()

    ###############################################################
    def add_note_to_listwidget(self, note):
        lw_item = QListWidgetItem(note.title)
        lw_item.note = note
        lw_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lw_notes.addItem(lw_item)

    def get_selected_lw_item(self):
        selected_items = self.lw_notes.selectedItems()
        if selected_items:
            return selected_items[0]
        return None


app = QApplication()
win = MainWindow()
win.show()
app.exec()
