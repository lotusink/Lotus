"""
This is an assistant can read your current screen and answer your question.
I call it LotusV1, but not finish yet.
"""

# TODO: Explore the possibility of using rule and model to adjust the behaviour of the LotusV1.
# TODO: This is not a critical TODO, but is inspired. Implement memory, topic consistency and 'emotion' by using engineer
#       method. Avoid too much spending.
# TODO: Consider add a function to use different large language model.
# TODO: Let printer can print LATEX code
# TODO: Calculator function

import sys

from scripts.Module import (
    ConnectOpenAI,
    ScreenCapturerClass,
    ModelObject,
    SendMessage
)
from PySide6.QtCore import (
    Qt,QRect
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
    QCheckBox,
    QGraphicsOpacityEffect,
    QHBoxLayout
)

from PySide6.QtGui import (
    QRegion,
    QPainterPath
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
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)
        # Set the background other than functional area to translucent background
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # The title
        self.setWindowTitle("Lotus")

        ### Initial the class
        # For model object
        self.model_object = model_object
        # For screen capturer object
        self.screen_capturer = screen_capturer

        ### Initial the value
        # For worker thread
        self.thread = None
        self.worker = None
        # For mouse dragging
        self._is_dragging = False
        self._drag_start_pos = None
        # For toggle visibility of label
        self._is_show = True

        ### For label
        self.label = QLabel("Good day, what`s on your mind?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("QLabel { background-color: transparent; color: white;}")


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

        ### For line editor and send button layout
        # TODO: Try using enter as the end of input
        self.container_line_send = QWidget()
        layout_line_send = QHBoxLayout()

        ### For line edit
        self.lineedit = QLineEdit()
        self.lineedit.setPlaceholderText("Ask anything")
        layout_line_send.addWidget(self.lineedit,stretch = 9)

        ### For button
        ## Sending
        self.button_send = QPushButton("Ask")
        # Once the button was clicked, send the prompt to the open API
        self.button_send.clicked.connect(self.trigger_message_sending_wrapper)
        self.button_send.setStyleSheet("QPushButton:disabled{background-color: unset}") # Unset: clear the custom color
        # Add to layout
        layout_line_send.addWidget(self.button_send, stretch = 1)
        # Add to widget
        self.container_line_send.setLayout(layout_line_send)
        ## Closing
        self.button_leave = QPushButton("Leave")
        self.button_leave.clicked.connect(self.close)
        # self.button_leave.setStyleSheet(
        #     "QPushButton {background-color:transparent; color:white; border: none}"
        #     "QPushButton:hover {background-color:grey; color:black; border-radius: 2px}"
        # )
        ## Hide and show layout
        self.button_hide_show = QPushButton("Show")
        self.button_hide_show.clicked.connect(self.toggle_visibility_label)

        ### For checkbox
        self.checkbox = QCheckBox("Using screenshot")
        # Default to False
        self.checkbox.setChecked(False)
        self.checkbox.checkStateChanged.connect(self.model_object.toggle_need_image)

        ### Checkbox, show and Closing button
        self.container_check_close = QWidget()
        self.layout_check_close = QHBoxLayout()
        self.layout_check_close.addWidget(self.checkbox,stretch = 2)
        self.layout_check_close.addWidget(self.button_hide_show, stretch=7)
        self.layout_check_close.addWidget(self.button_leave, stretch = 1)
        self.container_check_close.setLayout(self.layout_check_close)

        ### The main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.container_line_send)
        # mainLayout.addWidget(self.button_leave)
        # mainLayout.addWidget(self.button_hide_show)
        mainLayout.addWidget(self.container_check_close)
        mainLayout.addWidget(self.scrollArea)

        ### Container
        self.centralWidget = QWidget()
        self.centralWidget.setStyleSheet("{ background-color: transparent; color: white;}")
        self.centralWidget.setLayout(mainLayout)
        self.resize(600, 400)

        ### Set the page
        self.setCentralWidget(self.centralWidget)

        ### Set to round rectangle
        # Create a rectangle cover the whole window
        rect = QRect(0, 0, self.width(), self.height())
        # Create a painter object
        path = QPainterPath()
        # Add a rectangle to the painter object
        path.addRoundedRect(rect, 10, 10)  # 控制圆角半径
        # Transform the rectangle cover to round rectangle
        region = QRegion(
            path.toFillPolygon().toPolygon()
        )
        # Mask the whole window
        self.setMask(region)

    def mousePressEvent(self, event):
        """
        Judging whether the mouse has been pressed
        :param event: No idea
        :return:
        """
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._drag_start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """
        Judging whether the mouse is moving
        :param event:
        :return:
        """
        if self._is_dragging:
            self.move(event.globalPosition().toPoint() - self._drag_start_pos)

    def mouseReleaseEvent(self, event):
        """
        Judging whether the mouse has been released
        :return:
        """
        self._is_dragging = False

    def trigger_message_sending_wrapper(self):
        # Disable the button when running
        self.button_send.setText("Waiting...")
        self.button_send.setEnabled(False)
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
        self.thread.finished.connect(lambda :self.button_send.setEnabled(True))
        self.thread.finished.connect(lambda: self.button_send.setText("Send"))
        self.thread.start()

    def toggle_visibility_label(self):
        if self._is_show:
            self.scrollArea.setVisible(False)
            self.button_hide_show.setText("Show")
            for i in range(0,10):
                QApplication.processEvents()
            self.resize(self.width(),self.minimumSizeHint().height())
        else:
            self.scrollArea.setVisible(True)
            self.button_hide_show.setText("Hide")
            self.resize(600, 400)
        self._is_show = not self._is_show


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