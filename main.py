import sys
import os

import searcher
import hotkey_handler
from unity_searcher import UnitySearchModule

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QCoreApplication, Qt


# Allow QML to read from local files
os.environ['QML_XHR_ALLOW_FILE_READ'] = '1'

# Searcher setup
searcher.register_search_module(UnitySearchModule())

# Qt application setup
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load("file:///" + os.path.join(os.path.dirname(__file__), 'qml/main.qml'))
if not engine.rootObjects():
    sys.exit(-1)

hotkey_handler.start()

exit_code = app.exec()

hotkey_handler.stop()

sys.exit(exit_code)
