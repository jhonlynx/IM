import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

from backend.adminBack import adminPageBack

class AdminWorkersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def create_scrollable_cell(self, row, column, text):
        scrollable_widget = ScrollableTextWidget(text)
        self.workers_table.setCellWidget(row, column, scrollable_widget)     

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("WORKERS LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Search and Add button container
        search_add_layout = QtWidgets.QHBoxLayout() 
        
        # Search container
        search_container = QtWidgets.QHBoxLayout()
        
        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search workers by id...")
        self.search_input.textChanged.connect(self.filter_table)  # Add this line
        
        # Apply same styling to both widgets
        input_style = """
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """
        self.search_input.setStyleSheet(input_style)
        
        # Add widgets to container
        search_container.addWidget(self.search_input)
        
        search_add_layout.addLayout(search_container)
        
        # Add button with icon
        add_btn = QtWidgets.QPushButton("ADD WORKERS", icon=QtGui.QIcon("images/add.png"))
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
        add_btn.clicked.connect(self.show_add_workers_page)
        search_add_layout.addWidget(add_btn)
        
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)  



        # Table setup
        self.workers_table = QtWidgets.QTableWidget()
        self.workers_table.setAlternatingRowColors(True)
        self.workers_table.setStyleSheet("""
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
        self.workers_table.setColumnCount(3)
        self.workers_table.setHorizontalHeaderLabels([
            "ID", "NAME", "USERNAME"
        ])

        # Set the table to fill all available space
        self.workers_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.workers_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # Enable horizontal scrollbar
        self.workers_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.workers_table.setWordWrap(False)
        
        workers_back = adminPageBack()
        data = workers_back.fetch_users()
        
        self.populate_table(data)
        
        # Adjust table properties
        self.workers_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.workers_table.verticalHeader().setVisible(False)
        self.workers_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.workers_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        # Create a custom delegate for text elision with tooltip
        delegate = TextEllipsisDelegate(self.workers_table)
        self.workers_table.setItemDelegate(delegate)

        # Add table to the main layout with full expansion
        layout.addWidget(self.workers_table)


    def populate_table(self, data):
        self.workers_table.setRowCount(len(data))
        
        for row, employees in enumerate(data):
            # Unpack all values (now expecting 11 values in the customer tuple)
            user_id, name, username = employees

            # Add customer data to the table
            self.create_scrollable_cell(row, 0, str(user_id))
            self.create_scrollable_cell(row, 1, name)
            self.create_scrollable_cell(row, 2, username)

            # # Action buttons
            # actions_widget = QtWidgets.QWidget()
            # actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            # actions_layout.setContentsMargins(4, 4, 4, 4)
            
            # edit_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/edit.png"))
            # delete_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/delete.png"))
            
            # edit_btn.setIconSize(QtCore.QSize(24, 24))
            # delete_btn.setIconSize(QtCore.QSize(24, 24))
            
            # for btn in [edit_btn, delete_btn]:
            #     btn.setStyleSheet("""
            #         QPushButton {
            #             padding: 5px 10px;
            #             border: none;
            #             border-radius: 4px;
            #         }
            #         QPushButton:hover {
            #             background-color: #f0f0f0;
            #         }
            #     """)
            #     actions_layout.addWidget(btn)
            
            # self.customers_table.setCellWidget(row, 11, actions_widget)  # Place action buttons in the 11th column

    def show_add_workers_page(self):
        add_dialog = QtWidgets.QDialog(self)
        add_dialog.setWindowTitle("Add New Worker")
        add_dialog.setModal(True)
        add_dialog.setFixedSize(600, 400)
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

        # Section Title
        title = QtWidgets.QLabel("WORKER REGISTRATION FORM")
        title.setStyleSheet("font-size: 18px; padding: 10px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Form Layout
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

        def create_labeled_widget(label_text, widget):
            sub_layout = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            sub_layout.addWidget(label)
            sub_layout.addWidget(widget)
            return sub_layout

        # Input fields
        name_input = QtWidgets.QLineEdit()
        name_input.setStyleSheet(input_style)

        username_input = QtWidgets.QLineEdit()
        username_input.setStyleSheet(input_style)

        password_input = QtWidgets.QLineEdit()
        password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        password_input.setStyleSheet(input_style)

        conmfirmpassword_input = QtWidgets.QLineEdit()
        conmfirmpassword_input.setEchoMode(QtWidgets.QLineEdit.Password)
        conmfirmpassword_input.setStyleSheet(input_style)

        # Layout with labeled inputs
        form_layout.addLayout(create_labeled_widget("NAME:", name_input), 0, 0)
        form_layout.addLayout(create_labeled_widget("USERNAME:", username_input), 1, 0)
        form_layout.addLayout(create_labeled_widget("PASSWORD:", password_input), 2, 0)
        form_layout.addLayout(create_labeled_widget("CONFIRM PASSWORD:", conmfirmpassword_input), 3, 0)

        

        layout.addLayout(form_layout)

        # Spacer
        layout.addStretch()

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
        save_btn.clicked.connect(add_dialog.accept)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        add_dialog.exec_()

    # Add this new method
    def filter_table(self, text):
        search_text = text.lower()
        
        for row in range(self.workers_table.rowCount()):
            cell_widget = self.workers_table.cellWidget(row, 0)  # Get ID column widget
            if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
                worker_id = cell_widget.text().lower()
                if search_text in worker_id:
                    self.workers_table.setRowHidden(row, False)
                else:
                    self.workers_table.setRowHidden(row, True)
            else:
                self.workers_table.setRowHidden(row, True)    


class ScrollableTextWidget(QtWidgets.QWidget):
    
    def __init__(self, text, parent=None):
        super(ScrollableTextWidget, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scrollable text area
        self.text_area = QtWidgets.QScrollArea()
        self.text_area.setWidgetResizable(True)
        self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  
        self.text_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        # Create a label with the text
        self.label = QtWidgets.QLabel(text)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        # Add label to scroll area
        self.text_area.setWidget(self.label)
        
        # Add scroll area to layout
        layout.addWidget(self.text_area)
        
        # Set the widget's style
        self.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
            }
            QLabel {
                background-color: transparent;
                padding-left: 4px;
                padding-right: 4px;
            }
            QScrollBar:horizontal {
                height: 10px;
                background: transparent;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # Add tooltip for the full text
        self.setToolTip(text)

        # Install event filter to track mouse events
        self.installEventFilter(self)
        
    def text(self):
        return self.label.text()
    
    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QtCore.QEvent.Enter:
                # Show scrollbar when mouse enters
                self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                return True
            elif event.type() == QtCore.QEvent.Leave:
                # Hide scrollbar when mouse leaves
                self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                return True
        return super(ScrollableTextWidget, self).eventFilter(obj, event)


class TextEllipsisDelegate(QtWidgets.QStyledItemDelegate):
    
    def __init__(self, parent=None):
        super(TextEllipsisDelegate, self).__init__(parent)
        
    def paint(self, painter, option, index):
        # Use default painting
        super(TextEllipsisDelegate, self).paint(painter, option, index)
        
    def helpEvent(self, event, view, option, index):
        # Show tooltip when hovering if text is truncated
        if not event or not view:
            return False
            
        if event.type() == QtCore.QEvent.ToolTip:
            # Get the cell widget
            cell_widget = view.cellWidget(index.row(), index.column())
            
            if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
                # Show tooltip for ScrollableTextWidget
                QtWidgets.QToolTip.showText(event.globalPos(), cell_widget.text(), view)
                return True
            else:
                # For standard items
                item = view.itemFromIndex(index)
                if item:
                    text = item.text()
                    width = option.rect.width()
                    metrics = QtGui.QFontMetrics(option.font)
                    elidedText = metrics.elidedText(text, QtCore.Qt.ElideRight, width)
                    
                    # If text is truncated, show tooltip
                    if elidedText != text:
                        QtWidgets.QToolTip.showText(event.globalPos(), text, view)
                    else:
                        QtWidgets.QToolTip.hideText()
                    
                    return True
                
        return super(TextEllipsisDelegate, self).helpEvent(event, view, option, index)        


          


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AdminWorkersPage()
    window.show()
    sys.exit(app.exec_())
