class SearchModule:
    def __init__(self, name: str):
        self.name = name

    def setup(self) -> bool:
        print(self.name + ' failed to start')
        return False

    def search(self, query: str) -> list[dict]:
        pass  # Send error

    def get(self, id: object) -> str:
        pass  # Send error
