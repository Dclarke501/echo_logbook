import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Application")
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add a label
        label = QLabel("Hello from PySide6!")
        layout.addWidget(label)
        
        # Set window size
        self.setMinimumSize(400, 200)

if __name__ == "__main__":
    print("Starting application...")
    app = QApplication(sys.argv)
    print("Created QApplication")
    
    window = MainWindow()
    print("Created main window")
    
    window.show()
    print("Showing window")
    
    sys.exit(app.exec())