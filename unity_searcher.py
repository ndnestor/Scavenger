from bs4 import BeautifulSoup
from search_module import SearchModule
from lxml import etree
from lxml import html
import glob


# TODO: Make paths dynamic
documentation_path = './local_search_data/Documentation/en/ScriptReference/'
css_path = './css/unity.css'
max_results = 10 # TODO: Pull max results from settings


class UnitySearchModule(SearchModule):

    def __init__(self):
        super().__init__("Unity Local Search")

    def setup(self) -> bool:
        with open(css_path, encoding='utf-8') as css_file:
            self.css: list[str] = '\n'.join(css_file.readlines())

        return True

    def search(self, query: str) -> list[dict]:
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
                title = title_element.get_text().strip()
                
                # Get the preview text
                html_tree = html.fromstring(file_contents)
                description_node = html_tree.xpath('/html/body/div[3]/div[2]/div/div/div[1]/div[5]/p/node()')
                
                preview: str = ''
                for element in description_node:
                    element_type = type(element)
                    if element_type == etree._ElementUnicodeResult:
                        preview += element
                    elif element_type == html.HtmlElement:
                        if element.text != None:
                            preview += f'<code>{element.text}</code>'
                        else:
                            # TODO: Be more robust about this. Is there always a break tag when element.text == None?
                            break

                if description_node == None or preview == '':
                    preview = 'Preview not available'
                
                results.append({
                    'title': title,
                    'preview': preview,
                    'token': file_path
                })

            if len(results) == max_results:
                break
        
        # TODO: Don't return results without previews
        return results


    def get(self, token: str) -> str:
        with open(token, 'r', encoding='utf-8') as html_file:
            file_contents: object = html_file.read()
        
        # Remove extra info
        html_tree = etree.fromstring(file_contents)
        for element in html_tree.xpath('/html/body/div[2]/div[1]/div/div[1]/div'):
            element.getparent().remove(element)
        file_contents = str(etree.tostring(html_tree, pretty_print=True, method='html'))
        file_contents = file_contents.encode('ascii', 'ignore').decode('unicode_escape')[2:-1]
        
        # Inject CSS
        file_contents = file_contents.split('<head>', 1)
        file_contents[0] += f'<head>\n<style>\n{self.css}\n</style>\n'
        html = '<!DOCTYPE html>\n' + file_contents[0] + file_contents[1]

        return html


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
        for term in terms: # FIXME: Allow this to work with queries that include dots
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
