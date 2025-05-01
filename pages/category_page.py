import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

from backend.adminBack import adminPageBack

class CategoryPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("CATEGORIES LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Search and Add button container
        add_layout = QtWidgets.QHBoxLayout() 
        
        # Add button with icon
        add_btn = QtWidgets.QPushButton("ADD CATEGORY", icon=QtGui.QIcon("images/add.png"))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(229, 115, 115);
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
            QPushButton:hover {
                background-color: rgb(200, 100, 100);
            }
        """)
        add_btn.clicked.connect(self.show_add_category_page)
        add_layout.addWidget(add_btn)
        
        header_layout.addLayout(add_layout)
        layout.addLayout(header_layout)


        # Table setup
        self.categorys_table = QtWidgets.QTableWidget()
        self.categorys_table.setAlternatingRowColors(True)
        self.categorys_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #E8F5E9;
                alternate-background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
        """)
        
        # Set up columns (10 columns)
        self.categorys_table.setColumnCount(3)
        self.categorys_table.verticalHeader().setVisible(False)
        self.categorys_table.setHorizontalHeaderLabels([
            "ID", "NAME", "ACTION"
        ])
        
        category_back = adminPageBack()
        data = category_back.fetch_categories()
        
        self.populate_table(data)
        
        # Adjust table properties
        self.categorys_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.categorys_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.categorys_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.categorys_table)


    def populate_table(self, data):
        self.categorys_table.setRowCount(0)
        self.categorys_table.setRowCount(len(data))

        for row, category in enumerate(data):
            category_id, category_name = category

            self.categorys_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(category_id)))
            self.categorys_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(category_name)))

            # Action widget with deactivate and edit buttons
            actions_widget = QtWidgets.QWidget()
            actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(30)
            actions_layout.setAlignment(QtCore.Qt.AlignCenter)

            # Deactivate button
            deactivate_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/delete.png"))
            deactivate_btn.setIconSize(QtCore.QSize(24, 24))
            deactivate_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #fff0e0;
                }
            """)
            deactivate_btn.clicked.connect(lambda _, row=row: self.deactivate_category(row))

            # Edit button
            edit_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/edit.png"))
            edit_btn.setIconSize(QtCore.QSize(24, 24))
            edit_btn.setStyleSheet("""
                QPushButton {
                    padding: 5px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            edit_btn.clicked.connect(lambda _, row=row: self.show_edit_category_page(row))

            actions_layout.addWidget(deactivate_btn)
            actions_layout.addWidget(edit_btn)
            self.categorys_table.setCellWidget(row, 2, actions_widget)
 


    def show_add_category_page(self):
        add_dialog = QtWidgets.QDialog(self)
        add_dialog.setWindowTitle("New Category")
        add_dialog.setModal(True)
        add_dialog.setFixedSize(600, 200)
        add_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout(add_dialog)
        layout.setContentsMargins(30, 10, 30, 10)
        layout.setSpacing(10)

        # Title
        title = QtWidgets.QLabel("ADD NEW CATEGORY")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Form layout
        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(40)
        form_layout.setVerticalSpacing(20)

        input_style = """
            QLineEdit {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        # Create reusable label+input block
        def create_labeled_widget(label_text, widget):
            wrapper = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            wrapper.addWidget(label)
            wrapper.addWidget(widget)
            return wrapper

        # Category input
        category_name_input = QtWidgets.QLineEdit()
        category_name_input.setStyleSheet(input_style)

        form_layout.addLayout(create_labeled_widget("CATEGORY NAME:", category_name_input), 0, 0)

        layout.addLayout(form_layout)
        layout.addStretch()

        # Button container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(add_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        add_dialog.exec_()



    def show_edit_category_page(self, row):
        category_id = self.categorys_table.item(row, 0).text()
        current_name = self.categorys_table.item(row, 1).text()

        edit_dialog = QtWidgets.QDialog(self)
        edit_dialog.setWindowTitle("Edit Category")
        edit_dialog.setFixedSize(600, 250)
        edit_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout(edit_dialog)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        # Title
        title = QtWidgets.QLabel("EDIT CATEGORY")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Input styles
        input_style = """
            QLineEdit {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        # Create labeled widget helper
        def create_labeled_widget(label_text, widget):
            container = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            container.addWidget(label)
            container.addWidget(widget)
            return container

        # Form layout
        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(30)
        form_layout.setVerticalSpacing(15)

        name_input = QtWidgets.QLineEdit(current_name)
        name_input.setStyleSheet(input_style)

        form_layout.addLayout(create_labeled_widget("CATEGORY NAME:", name_input), 0, 0)

        layout.addLayout(form_layout)

        # Buttons
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(edit_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        edit_dialog.exec_()



    def deactivate_category(self, row):
        category_id = self.categorys_table.item(row, 0).text()

        reply = QtWidgets.QMessageBox.question(
            self, 'Deactivate Category',
            f"Are you sure you want to deactivate category ID {category_id}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )  

    

    def toggle_search_input(self, text):
            if text == "Category":
                self.search_input.hide()
                self.search_input_combo.show()
            else:
                self.search_input.show()
                self.search_input_combo.hide()           


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CategoryPage()
    window.show()
    sys.exit(app.exec_())
