from search_module import SearchModule

search_modules: list[SearchModule] = []


def register_search_module(search_module: SearchModule):
    print('Registering search module ' + search_module.name)
    if not search_module.setup():
        pass  # TODO: Send error
        return

    search_modules.append(search_module)


def search(query: str) -> list[dict]:
    for search_module in search_modules:
        return search_module.search(query)
