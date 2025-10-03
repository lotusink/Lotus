"""
This is an assistant can read your current screen and answer your question.
I call it LotusV1, but not finish yet.
"""

# TODO: Explore the possibility of using rule and model to adjust the behaviour of the LotusV1.
# TODO: This is not a critical TODO, but is inspired. Implement memory, topic consistency and 'emotion' by using engineer
#       method. Avoid too much spending.
# TODO: Consider add a function to use different large language model.
# TODO: 国内的模型用豆包试试
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
    Qt,
    QRect,
    QDate,
    QDateTime,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
)
from PyQt6.QtCore import (
    QThread,
    pyqtSignal,
    QCoreApplication
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform)
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
    QHBoxLayout,
    QFrame,
    QSizePolicy,
    QTextBrowser,
    QRadioButton
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

class MainMenu(QMainWindow):
    def __init__(
            self,
            model_object:ModelObject.Model,
            screen_capturer:ScreenCapturerClass.ScreenCapturer
        ):
        super().__init__()
        ### Set the windows pattern
        # Make sure my windows always stay on the top
        self.button_history = None
        self.button_send = None
        self.line_send_setting_3 = None
        self.button_leave = None
        self.button_hide_show = None
        self.line_send_setting_2 = None
        self.block_input = None
        self.input_line = None
        self.button_setting = None
        self.line_send_setting = None
        self.line_setting_leave = None
        self.scroll_area = None
        self.scrollAreaWidgetContents = None
        self.browser_text = None
        self.centralwidget = None
        self.block_outter = None
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # Set the background other than functional area to translucent background
        self.setAttribute(Qt.WA_TranslucentBackground)
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

        self.setupUi(self)
        self.define_function()

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1201, 575)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1201, 71))
        MainWindow.setMaximumSize(QSize(1201, 575))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.block_outter = QFrame(self.centralwidget)
        self.block_outter.setObjectName(u"block_outter")
        self.block_outter.setGeometry(QRect(0, 0, 1201, 571))
        self.block_outter.setStyleSheet(u"")
        self.block_outter.setFrameShape(QFrame.Shape.StyledPanel)
        self.block_outter.setFrameShadow(QFrame.Shadow.Raised)
        self.block_input = QFrame(self.block_outter)
        self.block_input.setObjectName(u"block_input")
        self.block_input.setGeometry(QRect(10, 10, 1181, 51))
        self.block_input.setFrameShape(QFrame.Shape.StyledPanel)
        self.block_input.setFrameShadow(QFrame.Shadow.Raised)
        self.input_line = QLineEdit(self.block_input)
        self.input_line.setObjectName(u"input_line")
        self.input_line.setGeometry(QRect(10, 10, 711, 31))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(12)
        font.setBold(False)
        self.input_line.setFont(font)
        self.input_line.setStyleSheet(u"border-radius: 0px")
        self.button_hide_show = QPushButton(self.block_input)
        self.button_hide_show.setObjectName(u"button_hide_show")
        self.button_hide_show.setGeometry(QRect(870, 10, 61, 31))
        font1 = QFont()
        font1.setFamilies([u"Wingdings 3"])
        font1.setPointSize(16)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setStrikeOut(False)
        self.button_hide_show.setFont(font1)
        self.button_hide_show.setStyleSheet(u"QPushButton {\n"
                                            "	background-color: transparent;\n"
                                            "	border: 0px;\n"
                                            "	border-radius: 5px 5px\n"
                                            "}\n"
                                            "QPushButton:hover {\n"
                                            "	background-color:rgb(99, 99, 99);\n"
                                            "	border: 5px\n"
                                            "}\n"
                                            "QPushButton:pressed {\n"
                                            "	background-color:rgb(67, 67, 67)\n"
                                            "}\n"
                                            "font:  \"Wingdings 3\";")
        self.button_setting = QPushButton(self.block_input)
        self.button_setting.setObjectName(u"button_setting")
        self.button_setting.setGeometry(QRect(1030, 10, 61, 31))
        font2 = QFont()
        font2.setFamilies([u"Wingdings"])
        font2.setPointSize(16)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setStrikeOut(False)
        self.button_setting.setFont(font2)
        self.button_setting.setStyleSheet(u"QPushButton {\n"
                                          "	background-color: transparent;\n"
                                          "	border: 0px;\n"
                                          "	border-radius: 5px 5px\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "	background-color:rgb(99, 99, 99);\n"
                                          "	border: 5px\n"
                                          "}\n"
                                          "QPushButton:pressed {\n"
                                          "	background-color:rgb(67, 67, 67)\n"
                                          "}\n"
                                          "QPushButton:checked {\n"
                                          "	background-color:rgb(145, 145, 145)\n"
                                          "}\n"
                                          "font:  \"Wingdings 3\";")
        self.button_setting.setCheckable(True)
        self.line_send_setting = QFrame(self.block_input)
        self.line_send_setting.setObjectName(u"line_send_setting")
        self.line_send_setting.setGeometry(QRect(1010, 10, 20, 31))
        self.line_send_setting.setFrameShape(QFrame.Shape.VLine)
        self.line_send_setting.setFrameShadow(QFrame.Shadow.Sunken)
        self.button_leave = QPushButton(self.block_input)
        self.button_leave.setObjectName(u"button_leave")
        self.button_leave.setGeometry(QRect(1110, 10, 61, 31))
        font3 = QFont()
        font3.setFamilies([u"Webdings"])
        font3.setPointSize(16)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStrikeOut(False)
        self.button_leave.setFont(font3)
        self.button_leave.setStyleSheet(u"QPushButton {\n"
                                        "	background-color: transparent;\n"
                                        "	border: 0px;\n"
                                        "	border-radius: 5px 5px\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "	background-color:rgb(99, 99, 99);\n"
                                        "	border: 5px\n"
                                        "}\n"
                                        "QPushButton:pressed {\n"
                                        "	background-color:rgb(67, 67, 67)\n"
                                        "}\n"
                                        "font:  \"Wingdings 3\";")
        self.line_setting_leave = QFrame(self.block_input)
        self.line_setting_leave.setObjectName(u"line_setting_leave")
        self.line_setting_leave.setGeometry(QRect(1090, 10, 20, 31))
        self.line_setting_leave.setFrameShape(QFrame.Shape.VLine)
        self.line_setting_leave.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_send_setting_2 = QFrame(self.block_input)
        self.line_send_setting_2.setObjectName(u"line_send_setting_2")
        self.line_send_setting_2.setGeometry(QRect(930, 10, 20, 31))
        self.line_send_setting_2.setFrameShape(QFrame.Shape.VLine)
        self.line_send_setting_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_send_setting_3 = QFrame(self.block_input)
        self.line_send_setting_3.setObjectName(u"line_send_setting_3")
        self.line_send_setting_3.setGeometry(QRect(850, 10, 20, 31))
        self.line_send_setting_3.setFrameShape(QFrame.Shape.VLine)
        self.line_send_setting_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.button_send = QPushButton(self.block_input)
        self.button_send.setObjectName(u"button_send")
        self.button_send.setGeometry(QRect(790, 10, 61, 31))
        self.button_send.setFont(font2)
        self.button_send.setStyleSheet(u"QPushButton {\n"
                                       "	background-color: transparent;\n"
                                       "	border: 0px;\n"
                                       "	border-radius: 5px 5px\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "	background-color:rgb(99, 99, 99);\n"
                                       "	border: 5px\n"
                                       "}\n"
                                       "QPushButton:pressed {\n"
                                       "	background-color:rgb(67, 67, 67)\n"
                                       "}\n"
                                       "font:  \"Wingdings 3\";")
        self.button_history = QPushButton(self.block_input)
        self.button_history.setObjectName(u"button_history")
        self.button_history.setGeometry(QRect(950, 10, 61, 31))
        self.button_history.setFont(font2)
        self.button_history.setStyleSheet(u"QPushButton {\n"
                                          "	background-color: transparent;\n"
                                          "	border: 0px;\n"
                                          "	border-radius: 5px 5px\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "	background-color:rgb(99, 99, 99);\n"
                                          "	border: 5px\n"
                                          "}\n"
                                          "QPushButton:pressed {\n"
                                          "	background-color:rgb(67, 67, 67)\n"
                                          "}\n"
                                          "QPushButton:checked {\n"
                                          "	background-color:rgb(145, 145, 145)\n"
                                          "}\n"
                                          "font:  \"Wingdings 3\";")
        self.button_history.setCheckable(True)
        self.scroll_area = QScrollArea(self.block_outter)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setGeometry(QRect(20, 90, 1161, 451))
        self.scroll_area.setStyleSheet(u"border-radius: 0px")
        self.scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1161, 451))
        self.browser_text = QTextBrowser(self.scrollAreaWidgetContents)
        self.browser_text.setObjectName(u"browser_text")
        self.browser_text.setGeometry(QRect(0, 0, 1161, 451))
        font4 = QFont()
        font4.setPointSize(12)
        self.browser_text.setFont(font4)
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.setWindowTitle("Lotus")
        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        # if QT_CONFIG(tooltip)
        self.input_line.setToolTip(
            QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        # endif // QT_CONFIG(tooltip)
        self.input_line.setText("")
        self.input_line.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ask anything...", None))
        # if QT_CONFIG(tooltip)
        self.button_hide_show.setToolTip(QCoreApplication.translate("MainWindow", u"Hiding the message", None))
        # endif // QT_CONFIG(tooltip)
        self.button_hide_show.setText(QCoreApplication.translate("MainWindow", u"p", None))
        # if QT_CONFIG(tooltip)
        self.button_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Using screenshot", None))
        # endif // QT_CONFIG(tooltip)
        self.button_setting.setText(QCoreApplication.translate("MainWindow", u"+", None))
        # if QT_CONFIG(tooltip)
        self.button_leave.setToolTip(QCoreApplication.translate("MainWindow", u"Leaving", None))
        # endif // QT_CONFIG(tooltip)
        self.button_leave.setText(QCoreApplication.translate("MainWindow", u"r", None))
        # if QT_CONFIG(tooltip)
        self.button_send.setToolTip(QCoreApplication.translate("MainWindow", u"Asking", None))
        # endif // QT_CONFIG(tooltip)
        self.button_send.setText(QCoreApplication.translate("MainWindow", u"*", None))
        # if QT_CONFIG(tooltip)
        self.button_history.setToolTip(QCoreApplication.translate("MainWindow", u"Using history", None))
        # endif // QT_CONFIG(tooltip)
        self.button_history.setText(QCoreApplication.translate("MainWindow", u"4", None))
        # retranslateUi

    # retranslateUi


    def define_function(self):
        self.button_send.clicked.connect(self.trigger_message_sending_wrapper)
        self.button_leave.clicked.connect(self.close)
        self.button_hide_show.clicked.connect(self.toggle_visibility_label)
        self.button_setting.toggled.connect(self.model_object.toggle_need_image)
        self.button_history.toggled.connect(self.model_object.toggle_need_history)


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
        self.button_send.setEnabled(False)
        self.input_line.setPlaceholderText(QCoreApplication.translate(
            "MainWindow", u"Please wait while I am thinking ....", None))
        self.thread = QThread(parent=None)
        # Get the prompt
        prompt = self.input_line.text()
        # Cleaning the input bar
        self.input_line.clear()
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
        self.worker.result.connect(lambda x: self.browser_text.setText(x))
        # Finish the running
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Setting the button back to active
        self.thread.finished.connect(lambda :self.button_send.setEnabled(True))
        self.thread.finished.connect(lambda: self.input_line.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"Ask anything...", None)))
        self.thread.start()

    def toggle_visibility_label(self):
        if self._is_show:
            self.scroll_area.setVisible(False)
            for i in range(0,10):
                QApplication.processEvents()
            self.block_outter.setGeometry(QRect(0, 0, 1201, 71))
            self.button_hide_show.setText(QCoreApplication.translate("MainWindow", u"q", None))
        else:
            self.scroll_area.setVisible(True)
            self.block_outter.setGeometry(QRect(0, 0, 1201, 571))
            self.button_hide_show.setText(QCoreApplication.translate("MainWindow", u"p", None))
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
    window = MainMenu(
        model_object=model_class,
        screen_capturer=ScreenCapturerClass.ScreenCapturer()
    )
    window.show()
    app.exec()