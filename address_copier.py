import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import Qt
import pandas as pd
import pyperclip

class DataEntryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Address Copier')
        self.setGeometry(100, 100, 500, 700)  # Adjusted window size for better fit
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # Window always on top

        # Determine the path to the CSV file relative to the script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(script_dir, "Housing_Hope_Developments.csv")

        # Load the data
        try:
            self.dataframe = pd.read_csv(csv_path)
        except FileNotFoundError:
            # Fallback for environments where __file__ might not be defined as expected
            try:
                self.dataframe = pd.read_csv("Housing_Hope_Developments.csv")
            except FileNotFoundError:
                print(f"Error: Housing_Hope_Developments.csv not found in {script_dir} or current directory.")
                sys.exit(1) # Exit if the file is not found


        # Main layout container widget
        main_container = QWidget()
        layout = QVBoxLayout(main_container)
        layout.setContentsMargins(10, 10, 10, 10) # Add some margins
        layout.setSpacing(5) # Add some spacing between rows
        self.setStyleSheet("background-color: #1a1a1a;")

        # Adding rows for each property
        for index, row in self.dataframe.iterrows():
            row_layout = QHBoxLayout()

            label = QLabel(str(row['Property Name'])) # Ensure property name is treated as string
            label.setStyleSheet("background-color: tan; padding: 5px; color: black; border-radius: 3px; min-width: 150px;")
            label.setToolTip(str(row['Property Name'])) # Show full name on hover if it's too long
            row_layout.addWidget(label)

            # Adding buttons for other columns
            for col_name in ['Line One', 'City', 'Zip']:
                btn = QPushButton(f"Copy {col_name}")
                # Styling for buttons
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #007fc5;
                        color: white;
                        padding: 5px;
                        border-radius: 3px;
                        min-width: 70px;
                    }
                    QPushButton:hover {
                        background-color: #005a8c;
                    }
                    QPushButton:pressed {
                        background-color: #003f63;
                    }
                """)
                # Ensure the value passed to the lambda is a string
                copy_value = str(row[col_name])
                btn.clicked.connect(lambda checked, value=copy_value: self.copy_to_clipboard(value))
                btn.setToolTip(f"Copy: {copy_value}") # Show what will be copied on hover
                row_layout.addWidget(btn)

            row_layout.addStretch() # Add stretch to push buttons to the left if window is wider
            layout.addLayout(row_layout)

        layout.addStretch(1) # Add a stretch at the end to push all content to the top

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(main_container)
        scroll_area.setStyleSheet("QScrollArea { border: none; }") # Remove scroll area border

        # Main layout for the QWidget (self)
        self_layout = QVBoxLayout(self)
        self_layout.addWidget(scroll_area)
        self_layout.setContentsMargins(0,0,0,0) # Remove margins for the main QWidget layout

    def copy_to_clipboard(self, content):
        try:
            pyperclip.copy(content)
            print(f"Copied: {content}")
        except pyperclip.PyperclipException as e:
            print(f"Error copying to clipboard: {e}")
            # Optionally, show a message box to the user
            # from PyQt5.QtWidgets import QMessageBox
            # QMessageBox.warning(self, "Clipboard Error", f"Could not copy to clipboard: {e}\nMake sure you have a copy/paste mechanism installed (e.g., xclip or xsel on Linux).")


if __name__ == '__main__':
    # Running the application
    app = QApplication(sys.argv)
    ex = DataEntryApp()
    ex.show()
    sys.exit(app.exec_())
