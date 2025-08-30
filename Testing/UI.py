# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainMenuhpsgSq.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QTextBrowser,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1201, 575)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1201, 71))
        MainWindow.setMaximumSize(QSize(1201, 575))
        MainWindow.setStyleSheet(u"background-color: rgba(44, 44, 44, 150)")
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

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.input_line.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.input_line.setText("")
        self.input_line.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ask anything...", None))
#if QT_CONFIG(tooltip)
        self.button_hide_show.setToolTip(QCoreApplication.translate("MainWindow", u"Hiding the message", None))
#endif // QT_CONFIG(tooltip)
        self.button_hide_show.setText(QCoreApplication.translate("MainWindow", u"p", None))
#if QT_CONFIG(tooltip)
        self.button_setting.setToolTip(QCoreApplication.translate("MainWindow", u"Using screenshot", None))
#endif // QT_CONFIG(tooltip)
        self.button_setting.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(tooltip)
        self.button_leave.setToolTip(QCoreApplication.translate("MainWindow", u"Leaving", None))
#endif // QT_CONFIG(tooltip)
        self.button_leave.setText(QCoreApplication.translate("MainWindow", u"r", None))
#if QT_CONFIG(tooltip)
        self.button_send.setToolTip(QCoreApplication.translate("MainWindow", u"Asking", None))
#endif // QT_CONFIG(tooltip)
        self.button_send.setText(QCoreApplication.translate("MainWindow", u"*", None))
#if QT_CONFIG(tooltip)
        self.button_history.setToolTip(QCoreApplication.translate("MainWindow", u"Using history", None))
#endif // QT_CONFIG(tooltip)
        self.button_history.setText(QCoreApplication.translate("MainWindow", u"4", None))
    # retranslateUi

