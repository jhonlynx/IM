import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

class AddWorkerPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(200, 50, 200, 50)
        layout.setSpacing(30)
        
        # Form container with green background
        form_container = QtWidgets.QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: #C9EBCB;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setVerticalSpacing(20)
        form_layout.setHorizontalSpacing(30)

        # Form title
        title = QtWidgets.QLabel("Add New Worker")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
            color: #333;
            text-align: center;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        form_layout.addWidget(title, 0, 0, 1, 2)

        # Input fields
        fields = [
            ("First Name", QtWidgets.QLineEdit()),
            ("Last Name", QtWidgets.QLineEdit()),
            ("Contact Number", QtWidgets.QLineEdit()),
            ("Username", QtWidgets.QLineEdit()),
            ("Password", QtWidgets.QLineEdit())
        ]
        
        # Set password field to password mode
        fields[4][1].setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Store input fields as instance variables
        self.first_name_input = fields[0][1]
        self.last_name_input = fields[1][1]
        self.contact_input = fields[2][1]
        self.username_input = fields[3][1]
        self.password_input = fields[4][1]

        # Add fields to form
        for row, (label_text, widget) in enumerate(fields, start=1):
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet("font-family: 'Roboto'; font-size: 14px;")
            widget.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-family: 'Roboto';
                }
            """)
            widget.setMinimumWidth(300)
            form_layout.addWidget(label, row, 0)
            form_layout.addWidget(widget, row, 1)

        # Button container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.setSpacing(15)

        # Back button
        back_btn = QtWidgets.QPushButton("Back")
        back_btn.setFixedSize(120, 35)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                font-family: 'Roboto';
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        back_btn.clicked.connect(lambda: self.parent.stacked_widget.setCurrentIndex(1))

        # Save button
        save_btn = QtWidgets.QPushButton("Save")
        save_btn.setFixedSize(120, 35)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(229, 115, 115);
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto';
            }
            QPushButton:hover {
                background-color: rgb(200, 100, 100);
            }
        """)
        save_btn.clicked.connect(self.save_worker)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(save_btn)

        # Add button container to form layout
        form_layout.addWidget(button_container, len(fields)+1, 0, 1, 2, QtCore.Qt.AlignCenter)

        layout.addWidget(form_container)

    def save_worker(self):
        # TODO: Implement save functionality
        pass