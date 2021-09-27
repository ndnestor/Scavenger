from bs4 import BeautifulSoup
from search_module import SearchModule
from lxml import html
import glob


documentation_path = 'D:/OneDrive - Rutgers University/Programming/Scavenger/Local Search Data/Documentation/en/ScriptReference/'
max_results = 10

class UnitySearchModule(SearchModule):

    def __init__(self):
        super().__init__("Unity Local Search")

    def setup(self) -> bool:
        return True

    def search(self, query: str) -> list[dict]:
        print('Searching for ' + query)
        results: list[dict] = []

        file_paths: list[str] = glob.glob(documentation_path + "*" + query + '*.html', recursive=True)
        file_paths = sort_file_paths(file_paths, query)
        for file_path in file_paths:
            with open(file_path, encoding='utf-8') as file:
                file_contents = file.read()

                # Get the title text
                html_soup = BeautifulSoup(file_contents, 'html.parser')
                title_element = html_soup.find('h1', class_='heading inherit')
                if title_element == None:
                    continue
                title = title_element.get_text()
                
                # Get the preview text
                html_tree = html.fromstring(file_contents)
                preview = html_tree.xpath('/html/body/div[3]/div[2]/div/div/div[1]/div[5]/p/text()')
                if preview == None:
                    preview = 'Preview not available'
                
                results.append({
                    'title': title,
                    'preview': preview
                })

            if len(results) == max_results:
                break
        
        for result in results:
            print(result['title'])
        return results

def sort_file_paths(file_paths: list[str], query: str) -> list[str]:

    sorted_file_paths_collapsed: list[list[str]] = []
    
    for file_path in file_paths:

        # Get file name
        file_name: str
        for i in reversed(range(len(file_path))):
            if file_path[i] == '\\' or file_path[i] == '/':
                file_name = file_path[i + 1:len(file_path) - len('.html')]
                break
        
        # Add file name to collapsed list
        terms: list[str] = file_name.split('.')
        priority_value: int = None
        for term in terms:            
            try:
                possible_priority_value: int = term.lower().index(query.lower())
            except:
                continue

            if priority_value == None or priority_value > possible_priority_value:
                priority_value = possible_priority_value

        while len(sorted_file_paths_collapsed) - 1 < priority_value:
            sorted_file_paths_collapsed.append([])
        
        sorted_file_paths_collapsed[priority_value].append(file_path)

    # Uncollapse the list
    sorted_file_paths: list[str] = []
    for file_path_list in sorted_file_paths_collapsed:
        for file_path in file_path_list:
            sorted_file_paths.append(file_path)
    
    return sorted_file_paths
