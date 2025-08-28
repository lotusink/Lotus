"""
This is an assistant can read your current screen and answer your question.
I call it LotusV1, but not finish yet.
"""

import sys
from Testing.Module import (
    ConnectOpenAI,
    ImageOpenAIApi
)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QScrollArea
)

from Testing.Module.SendMessageToOpenAI import Model


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ### Set the windows pattern
        # Make sure my windows always stay on the top
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # TODO: Adding mouse dragging function also the close function in translucent background
        # self.setWindowFlag(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # Set the background other than functional area to translucent background
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # The title
        self.setWindowTitle("Learning Assistant")

        ### Initial the class value

        ### For line edit
        self.lineedit = QLineEdit()
        self.lineedit.setPlaceholderText("What do you want to ask about your current screen?")

        ### For label
        self.label = QLabel("Wait for your command!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)

        ## For scrollable area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        ## For mini container of scrollable area
        # Creating a mini container
        container = QWidget()
        # Create a new vertical layout
        layout = QVBoxLayout()
        # Add the label into this layout
        layout.addWidget(self.label)
        # Add it to the container
        container.setLayout(layout)
        # Add it to the scrollable area
        self.scrollArea.setWidget(container)

        ### For button
        self.button = QPushButton("Send...")
        self.button.setCheckable(True)
        # Once the button was clicked, send the prompt to the open API
        self.button.clicked.connect(self.activate_agent)

        ### The main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.scrollArea)
        mainLayout.addWidget(self.lineedit)
        mainLayout.addWidget(self.button)

        ### Container
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        centralWidget.setMinimumSize(480, 320)


        ### Set the page
        self.setCentralWidget(centralWidget)

    def activate_agent(self):
        # TODO: Optimize the running logic to avoid the block of the main thread
        # Update the prompt list through the output of the lineedit text
        model_object.update_prompt_list(self.lineedit.text())
        # Clean the content
        self.lineedit.clear()
        # Sent the text to the agent
        response = ConnectOpenAI.main(prompt=self.prompt)
        # Delete the text in the lineedit
        self.label.setText(response)




if __name__ == "__main__":
    ### Connect to the OpenAI API
    client = ConnectOpenAI.connect_openai_api()

    ### Create a Model object
    model_object = Model(client=client)

    ### Start the service
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()