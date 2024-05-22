import os
import shutil
import sys
import PyInstaller.__main__
from PyQt5.QtCore import Qt
from git import Repo
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, \
    QPushButton, QProgressBar

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

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("V8 Launcher")
        self.setGeometry(1200, 600, 1200, 900)
        self.setStyleSheet(dark_mode_style)
        self.username = 'V8Enthusiast'

        self.buttons = ["Launch", "Update", "Remove"]
        self.checkboxes = ["Tetris", "Minesweeper", "2048", "File Explorer", "Sandbox"]

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
        self.checkbox_objects = []
        for name in self.checkboxes:
            checkbox = QCheckBox(name)
            checkbox.setStyleSheet("QCheckBox::indicator { width: 30px; height: 30px;}")
            checkbox.setFont(QFont("Arial", 24))  # Set a larger font size
            #checkbox.setFixedSize(350, 40)  # Set a larger size for the checkbox
            self.checkbox_objects.append(checkbox)
            checkbox_list.addWidget(checkbox)

        button_layout = QHBoxLayout()

        # Create a container widget to hold the checkbox list
        checkbox_container = QWidget()
        checkbox_container.setLayout(checkbox_list)

        layout2.addWidget(checkbox_container)

        spacer_item = QWidget()
        spacer_item.setFixedHeight(20)

        layout2.addWidget(spacer_item)

        for name in self.buttons:
            button = QPushButton(name)
            button.setFont(QFont("Arial", 36))
            if name == 'Launch':
                button.clicked.connect(self.launch_apps)
            elif name == 'Update':
                button.clicked.connect(self.update_apps)
            elif name == 'Remove':
                button.clicked.connect(self.remove_apps)
            # button.setStyleSheet(
            #     "background-color: #c6e2ff; border: 1px solid #4d94ff; border-radius: 10px; padding: 5px;"
            #     "QPushButton:hover { background-color: #ffffff; }"
            #     "QPushButton:pressed { background-color: #85a9ff; }"
            # )
            button_layout.addWidget(button)

        layout2.addLayout(button_layout)  # Add the button layout under the checkbox list

        spacer_item = QWidget()
        spacer_item.setFixedHeight(20)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        self.progress_bar.setStyleSheet("QProgressBar {"
                                        "border: 2px solid grey;"
                                        "border-radius: 5px;"
                                        "text-align: center;"
                                        "color: white;"
                                        "background-color: #333;"
                                        "}"
                                        "QProgressBar::chunk {"
                                        "background-color: #2B5DD1;"
                                        "}")

        layout2.addWidget(self.progress_bar)

        self.label_status = QLabel("Ready")
        self.label_status.setAlignment(Qt.AlignCenter)
        layout2.addWidget(self.label_status)

        # Add stretch to fill the left part of the screen
        layout2.addStretch()

        tab2.setLayout(layout2)

        self.setCentralWidget(tab_widget)

    def launch_apps(self):
        sender = self.sender()  # Get the button that was clicked
        checked_checkboxes = [checkbox.text() for checkbox in self.checkbox_objects if checkbox.isChecked()]
        print(f"Launching {checked_checkboxes}")
        for project in checked_checkboxes:
            try:
                os.chdir(f'{project}')
                os.startfile(f'main.exe')
                os.chdir('..')
                print(f"Launching {project}")
            except Exception as e:
                print(f"Failed: {e}")
    def update_apps(self):
        sender = self.sender()  # Get the button that was clicked
        print(f"Updating")
        checked_checkboxes = [checkbox.text() for checkbox in self.checkbox_objects if checkbox.isChecked()]
        total_steps = 5
        for repo_name in checked_checkboxes:
            step = 0
            self.update_progress(step, total_steps)
            try:
                #self.label_status.setText(f"Updating {repo_name}...")
                local_path = f'{repo_name}'
                self.label_status.setText(f"Removing old version...")
                delete_folder(local_path)

                self.update_progress(step, total_steps)
                step += 1
                self.label_status.setText(f"Downloading {repo_name} from GitHub...")

                repo_url = f'https://github.com/{self.username}/{repo_name}.git'

                # Clone the repository
                Repo.clone_from(repo_url, local_path)

                self.update_progress(step, total_steps)
                step += 1
                self.label_status.setText(f"Building executable...")

                #if os.path.exists(local_path + '/img') and os.path.isdir(local_path + '/img'):
                opts = [f'{local_path}\main.py', '--windowed']

                # Build the executable using PyInstaller
                PyInstaller.__main__.run(opts)

                self.update_progress(step, total_steps)
                step += 1
                self.label_status.setText(f"Clearing directory...")

                delete_py_files(local_path)

                self.update_progress(step, total_steps)
                step += 1
                self.label_status.setText(f"Moving files...")

                move_contents('dist\main', local_path)

                self.update_progress(step, total_steps)
                step += 1
                self.label_status.setText(f"Removing temporary files...")

                delete_folder('build')
                delete_folder('dist')
                os.remove('main.spec')

                self.update_progress(step, total_steps)
                self.label_status.setText(f"Ready")



            except Exception as e:
                print(f"Failed: {e}")
                self.update_progress(0, total_steps)
                self.label_status.setText(f"Update Failed")

    def update_progress(self, current_step, total_steps):
        progress = int((current_step / total_steps) * 100)
        self.progress_bar.setValue(progress)

    def remove_apps(self):
        sender = self.sender()  # Get the button that was clicked
        print(f"Removing")

def delete_folder(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Folder {path} has been deleted.")
        except Exception as e:
            print(f"Failed to delete {path}. Reason: {e}")
    else:
        print(f"Folder {path} does not exist.")
def delete_py_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete: {file_path}. Reason: {e}")
def move_contents(source, destination):
    # Check if both folders exist
    if os.path.exists(source) and os.path.exists(destination):
        # Iterate over the files in the source folder and move them to the destination folder
        for filename in os.listdir(source):
            source_file = os.path.join(source, filename)
            destination_file = os.path.join(destination, filename)
            try:
                shutil.move(source_file, destination_file)
                print(f"Moved {source_file} to {destination_file}")
            except Exception as e:
                print(f"Failed to move {source_file}. Reason: {e}")
        print("All contents moved successfully.")
    else:
        print("Source or destination folder does not exist.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 14))
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())