import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, \
    QPushButton

chrome_tab_style = """
QTabBar::tab {
    background-color: #f0f0f0;
    color: #333;
    border: 1px solid #ccc;
    border-bottom-color: #aaa;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 80px;
    padding: 4px;
}

QTabBar::tab:selected {
    background-color: #fff;
    border-bottom-color: #fff;
}
"""

chrome_tab_style_dark = """
QTabBar::tab {
    background-color: #333;
    color: #f0f0f0;
    border: 1px solid #555;
    border-bottom-color: #777;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 80px;
    padding: 4px;
}

QTabBar::tab:selected {
    background-color: #222;
    border-bottom-color: #222;
}
"""

dark_mode_style = """
QWidget {
    border: none;
    background-color: #333;
    color: #f0f0f0;
}

QLabel {
    color: #f0f0f0;
}

QCheckBox {
    color: #f0f0f0;
    background-color: #333;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 4px;
}

QCheckBox::indicator {
    width: 30px;
    height: 30px;
}
QTabWidget::pane{
    border:none
}

QPushButton {
    background-color: #2B5DD1;
    color: #FFFFFF;
    border-style: none;
    padding: 22px;
    font: bold 36px;
    
    border-radius: 10px;
    border-color: #2752B8;
}
QPushButton:hover {
    background-color: #f0f0f0;
    color: #333
}
"""

# Apply dark mode style to the main window and its components

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("V8 Launcher")
        self.setGeometry(1200, 600, 1200, 900)
        self.setStyleSheet(dark_mode_style)

        self.buttons = ["Launch", "Update", "Remove"]
        self.checkboxes = ["Tetris", "Minesweeper", "2048", "File Commander", "Sandbox"]

        tab_widget = QTabWidget()

        tab_widget.setStyleSheet(chrome_tab_style_dark)

        tab1 = QWidget()
        tab2 = QWidget()

        tab_widget.addTab(tab1, "Downloads")
        tab_widget.addTab(tab2, "Library")

        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("Download Page"))
        tab1.setLayout(layout1)

        layout2 = QVBoxLayout()

        label_tab2 = QLabel("Available apps:")
        layout2.addWidget(label_tab2)

        checkbox_list = QVBoxLayout()
        checkboxes = []
        for name in self.checkboxes:
            checkbox = QCheckBox(name)
            checkbox.setStyleSheet("QCheckBox::indicator { width: 30px; height: 30px;}")
            checkbox.setFont(QFont("Arial", 24))  # Set a larger font size
            #checkbox.setFixedSize(350, 40)  # Set a larger size for the checkbox
            checkboxes.append(checkbox)
            checkbox_list.addWidget(checkbox)

        button_layout = QHBoxLayout()  # Create a horizontal layout for the buttons

        # Create a container widget to hold the checkbox list
        checkbox_container = QWidget()
        checkbox_container.setLayout(checkbox_list)

        layout2.addWidget(checkbox_container)

        spacer_item = QWidget()
        spacer_item.setFixedHeight(20)  # Set the desired height for the space

        layout2.addWidget(spacer_item)

        # Create and add 3 buttons to the layout
        for name in self.buttons:
            button = QPushButton(name)
            # Inside the loop where buttons are created
            button.setFont(QFont("Arial", 36))
            button.clicked.connect(self.button_clicked)  # Connect the button to a function
            # button.setStyleSheet(
            #     "background-color: #c6e2ff; border: 1px solid #4d94ff; border-radius: 10px; padding: 5px;"
            #     "QPushButton:hover { background-color: #ffffff; }"
            #     "QPushButton:pressed { background-color: #85a9ff; }"
            # )
            button_layout.addWidget(button)

        layout2.addLayout(button_layout)  # Add the button layout under the checkbox list

        # Add stretch to fill the left part of the screen
        layout2.addStretch()

        tab2.setLayout(layout2)

        self.setCentralWidget(tab_widget)

    # Define a function to handle button clicks
    def button_clicked(self):
        sender = self.sender()  # Get the button that was clicked
        print(f"Button {sender.text()} was clicked")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 14))
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())