"""
This is an assistant can read your current screen and answer your question.
I call it LotusV1, but not finish yet.
"""

# TODO: Explore the possibility of using rule and model to adjust the behaviour of the LotusV1.
# TODO: This is not a critical TODO, but is inspired. Implement memory, topic consistency and 'emotion' by using engineer
#       method. Avoid too much spending.

import sys

from Testing.Module import (
    ConnectOpenAI,
    ScreenCapturerClass,
    ModelObject,
    SendMessage
)
from PySide6.QtCore import (
    Qt
)
from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QScrollArea,
    QCheckBox
)

class Worker(QThread):
    """
    A class using to implement worker thread for api requesting.
    """
    result = pyqtSignal(object,name="result")
    finished = pyqtSignal(name="finished")

    def __init__(
            self,
            screen_capturer: ScreenCapturerClass.ScreenCapturer,
            model_object: ModelObject.Model,
            prompt
    ):
        super().__init__(parent=None)
        self.prompt = prompt
        self.screen_capturer = screen_capturer
        self.model_object = model_object

    def run(self):
        try:
            # Get the screenshot
            self.screen_capturer.get_screenshot()
            # Update the prompt list through the output of the lineedit text
            self.model_object.update_prompt_list_user(
                prompt=self.prompt,
                b64_image=self.screen_capturer.get_image(),
            )
            # Sent the text to the agent
            response = SendMessage.send_receive_message(self.model_object)
            # Update the agent response
            self.model_object.update_prompt_list_agent(agent_response=response)
            # Sent back the result
            self.result.emit(response)
        except Exception as e:
            print(f"Error in Worker: {e}")
        finally:
            # Finish
            self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(
            self,
            model_object:ModelObject.Model,
            screen_capturer:ScreenCapturerClass.ScreenCapturer
        ):
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

        ### Initial the class
        # For model object
        self.model_object = model_object
        # For screen capturer object
        self.screen_capturer = screen_capturer

        ### Initial the value
        # For worker thread
        self.thread = None
        self.worker = None

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
        self.button = QPushButton("Send")
        # Once the button was clicked, send the prompt to the open API
        self.button.clicked.connect(self.trigger_message_sending_wrapper)

        ### For checkbox
        self.checkbox = QCheckBox("Using screenshot")
        # Default to False
        self.checkbox.setChecked(False)
        self.checkbox.checkStateChanged.connect(self.model_object.toggle_need_image)

        ### The main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.scrollArea)
        mainLayout.addWidget(self.lineedit)
        mainLayout.addWidget(self.button)
        mainLayout.addWidget(self.checkbox)

        ### Container
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        centralWidget.setMinimumSize(480, 320)


        ### Set the page
        self.setCentralWidget(centralWidget)

    def trigger_message_sending_wrapper(self):
        # Disable the button when running
        self.button.setEnabled(False)
        self.button.setText("Please waiting...")
        self.thread = QThread(parent=None)
        # Get the prompt
        prompt = self.lineedit.text()
        # Cleaning the input bar
        self.lineedit.clear()
        # Create a worker object
        self.worker = Worker(
            screen_capturer=self.screen_capturer,
            model_object=self.model_object,
            prompt=prompt
        )
        # Move to thread
        self.worker.moveToThread(self.thread)
        # Running
        self.thread.started.connect(self.worker.run)
        # Return the response
        self.worker.result.connect(lambda x: self.label.setText(x))
        # Finish the running
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Setting the button back to active
        self.thread.finished.connect(lambda :self.button.setEnabled(True))
        self.thread.finished.connect(lambda: self.button.setText("Send"))
        self.thread.start()

if __name__ == "__main__":
    ### Initial class
    # Model
    model_class = ModelObject.Model()

    ### Connect to the OpenAI API
    ConnectOpenAI.connect_openai_api(
        model_object=model_class
    )

    ### Start the service
    app = QApplication(sys.argv)
    window = MainWindow(
        model_object=model_class,
        screen_capturer=ScreenCapturerClass.ScreenCapturer()
    )
    window.show()
    app.exec()