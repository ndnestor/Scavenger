import sys
import os

import searcher
from unity_searcher import UnitySearchModule

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject, Property

searcher.register_search_module(UnitySearchModule())

class Searcher(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._query = ''
     
    @Property('QString')
    def query(self):
        return self._query
    
    @query.setter
    def query(self, query):
        if self._query == query:
            return
        
        self._query = query

        search_results: list[dict] = searcher.search(query)

        # Display search results
        for search_result in search_results:
            pass


app = QGuiApplication(sys.argv)

qmlRegisterType(Searcher, 'Searcher', 1, 0, 'Searcher')

engine = QQmlApplicationEngine()
engine.load(os.path.join(os.path.dirname(__file__), 'qml/main.qml'))

if not engine.rootObjects():
    sys.exit(-1)
sys.exit(app.exec())
