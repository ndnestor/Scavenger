from search_module import SearchModule

from types import FunctionType

from PySide6.QtQml import qmlRegisterType
from PySide6.QtCore import QObject, Property, QThread, Signal


search_modules: list[SearchModule] = []


def register_search_module(search_module: SearchModule):
    print('Registering search module ' + search_module.name)
    if not search_module.setup():
        pass  # TODO: Send error
        return

    search_modules.append(search_module)


def search(query: str) -> list[dict]:
    print('Searching for ' + query)
    for search_module in search_modules:
        return search_module.search(query)


class Searcher(QObject):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._query: str = ''
        self._search_results: list[dict] = []
        self._results_have_changed: bool = False
        self._cards: list = []
        self.last_searched_query: str = ''

        def search_work() -> None:
            self._search_results = search(self.query)
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

qmlRegisterType(Searcher, 'Searcher', 1, 0, 'Searcher')
