import sys
import os
from types import FunctionType

import searcher
from unity_searcher import UnitySearchModule

import hotkey_handler

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import QObject, Property, QThread, Signal


# Searcher setup
searcher.register_search_module(UnitySearchModule())


class Searcher(QObject):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._query: str = ''
        self._search_results: list[dict] = []
        self._results_have_changed: bool = False
        self._cards: list = []
        self.last_searched_query: str = ''

        def search_work() -> None:
            self._search_results = searcher.search(self.query)
            self._results_have_changed = True

        self.search_worker = Worker(search_work)
        self.search_thread = QThread()
        self.search_worker.moveToThread(self.search_thread)
        self.search_thread.started.connect(self.search_worker.run)
        self.search_worker.finished.connect(self.search_thread.quit)

    @Property(list)
    def cards(self) -> list:
        return self._cards
    
    @cards.setter
    def cards(self, cards: list) -> None:
        self._cards = cards
    
    @Property(bool)
    def results_have_changed(self) -> bool:
        return self._results_have_changed
    
    @results_have_changed.setter
    def results_have_changed(self, results_have_changed: bool) -> None:
        self._results_have_changed = results_have_changed

    @Property(list)
    def search_results(self) -> list[dict]:
        return self._search_results
    
    @Property(str)
    def query(self) -> str:
        return self._query
    
    @query.setter
    def query(self, query: str) -> None:

        self._query = query

        # Search if query has not been searched yet and thread is not in progress
        if not self.search_thread.isRunning():
            if not self.last_searched_query == query:
                self.last_searched_query = query
                self.search_thread.start()


class Worker(QObject):
    finished = Signal()
    
    def __init__(self, work: FunctionType, parent=None) -> None:
        super().__init__(parent)
        self.work = work

    def run(self) -> None:
        self.work()
        self.finished.emit()


# Qt application setup
app = QGuiApplication(sys.argv)

qmlRegisterType(Searcher, 'Searcher', 1, 0, 'Searcher')

engine = QQmlApplicationEngine()
engine.load(os.path.join(os.path.dirname(__file__), 'qml/main.qml'))

if not engine.rootObjects():
    sys.exit(-1)

hotkey_handler.start()

exit_code = app.exec()

hotkey_handler.stop()

sys.exit(exit_code)
