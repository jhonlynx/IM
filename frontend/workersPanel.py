import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtGui, QtWidgets
from pages.employee_customers_page import EmployeeCustomersPage
from pages.billing_page import EmployeeBillingPage
from pages.category_page import CategoryPage
from pages.address_page import AddressPage
from pages.transactions_page import TransactionsPage

class WorkersPanel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOWBASCO - Workers Panel")
        self.setMinimumSize(1200, 800)
        self.showMaximized()
        
        # Main widget and layout setup
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create sidebar
        self.setup_sidebar()
        
        # Create stacked widget and header
        self.setup_main_content()
        
        # Initialize pages
        self.initialize_pages()
        
        # Set initial page
        self.stacked_widget.setCurrentIndex(0)

    def setup_main_content(self):
        # Create stacked widget for different pages
        self.stacked_widget = QtWidgets.QStackedWidget()
        
        # Create green header bar
        header_bar = QtWidgets.QWidget()
        header_bar.setStyleSheet("background-color: rgb(201, 235, 203);")
        header_bar.setFixedHeight(70)
        
        header_layout = QtWidgets.QHBoxLayout(header_bar)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        full_name = QtWidgets.QLabel("SouthWestern Barangays Water Services Cooperative II")
        full_name.setStyleSheet("""
            color: rgb(60, 60, 60);
            font-size: 16px;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
        """)
        full_name.setAlignment(QtCore.Qt.AlignCenter)
        header_layout.addWidget(full_name)
        
        # Create container for stacked widget and header
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        container_layout.addWidget(header_bar)
        container_layout.addWidget(self.stacked_widget)
        
        self.main_layout.addWidget(container)

    def initialize_pages(self):
        # Initialize all pages
        self.customers_page = EmployeeCustomersPage(self)
        self.category_page = CategoryPage(self)
        self.address_page = AddressPage(self)
        self.billing_page = EmployeeBillingPage(self)
        self.transactions_page = TransactionsPage(self)
        
        # Add pages to stacked widget     # Index 0
        self.stacked_widget.addWidget(self.customers_page)     
        self.stacked_widget.addWidget(self.category_page) 
        self.stacked_widget.addWidget(self.address_page) 
        self.stacked_widget.addWidget(self.billing_page)       
        self.stacked_widget.addWidget(self.transactions_page)  

    def setup_sidebar(self):
        sidebar = QtWidgets.QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: rgb(201, 235, 203);
                border: none;
            }
            QPushButton {
                text-align: left;
                padding: 15px 20px;
                border: none;
                border-radius: 0;
                font-size: 16px;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E8F8E4;
            }
            QPushButton:checked {
                background-color: #E8F8E4;
            }
        """)
        sidebar.setFixedWidth(250)
        
        # Create sidebar layout
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo and text container
        header_layout = QtWidgets.QHBoxLayout()
        
        # Logo image
        logo_image = QtWidgets.QLabel()
        logo_pixmap = QtGui.QPixmap("images/logosowbasco.png")
        scaled_pixmap = logo_pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        logo_image.setPixmap(scaled_pixmap)
        logo_image.setStyleSheet("padding: 10px;")
        header_layout.addWidget(logo_image)
        
        # Title text
        logo_label = QtWidgets.QLabel("SOWBASCO")
        logo_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            font-family: 'Montserrat', sans-serif;
        """)
        header_layout.addWidget(logo_label)
        
        sidebar_layout.addLayout(header_layout)
        
        # Navigation buttons
        self.nav_buttons = []
        for text, icon_path in [
            ("Customers", "images/clients.png"),
            ("Categories", "images/category.png"),
            ("Address", "images/address.png"),
            ("Billing", "images/bill.png"),
            ("Transactions", "images/transaction.png")
        ]:
            btn = QtWidgets.QPushButton(text)
            btn.setIcon(QtGui.QIcon(icon_path))
            btn.setIconSize(QtCore.QSize(50, 50))
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, x=text: self.change_page(x))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        # Add stretch to push logout to bottom
        sidebar_layout.addStretch()
        
        # Logout button
        logout_btn = QtWidgets.QPushButton("Logout")
        logout_btn.setIcon(QtGui.QIcon("images/logout.png"))
        logout_btn.setIconSize(QtCore.QSize(50, 50))
        logout_btn.clicked.connect(self.logout)  # Add this line
        sidebar_layout.addWidget(logout_btn)
        
        self.main_layout.addWidget(sidebar)
        self.nav_buttons[0].setChecked(True)

    def logout(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Logout")
        dialog.setFixedWidth(400)
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;  /* Changed to match the green theme */
                border-radius: 10px;
            }
            QLabel {
                font-family: 'Roboto', sans-serif;
                color: #333;
            }
            QPushButton {
                padding: 8px 20px;
                font-family: 'Roboto', sans-serif;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton#confirm {
                background-color: rgb(229, 115, 115);
                color: white;
                border: none;
            }
            QPushButton#confirm:hover {
                background-color: rgb(200, 100, 100);
            }
            QPushButton#cancel {
                background-color: #6c757d;
                border: 1px solid #ddd;
                color: white;
            }
            QPushButton#cancel:hover {
                background-color: #5a6268;
            }
        """)

        # Dialog layout
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Message
        message = QtWidgets.QLabel("Confirm Logout?")
        message.setStyleSheet("font-size: 16px; font-weight: bold; text-align: center;")
        message.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(message)

        # Buttons layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)

        # Cancel button
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setObjectName("cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        # Confirm button
        confirm_btn = QtWidgets.QPushButton("Confirm")
        confirm_btn.setObjectName("confirm")
        confirm_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(confirm_btn)

        layout.addLayout(button_layout)

        # Show dialog and handle result
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            from frontend.login import LoginWindow
            self.login = LoginWindow()
            self.login.show()
            self.close()


    def change_page(self, page_name):
        # Uncheck all buttons except the clicked one
        for btn in self.nav_buttons:
            if page_name not in btn.text():
                btn.setChecked(False)
        
        # Change stacked widget page
        page_index = {
            "Customers": 0,
            "Categories": 1,
            "Address": 2,
            "Billing": 3,
            "Transactions": 4
        }
        
        if page_name in page_index:
            self.stacked_widget.setCurrentIndex(page_index[page_name])   



# Add this at the very end of the file:
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = WorkersPanel()
    window.show()
    sys.exit(app.exec_())