from datetime import datetime
from pathlib import Path
import uuid

directive_symbol_start = '<!--$'
directive_symbol_end = '$-->'
timestamp_format = '%m-%d-%YT%H:%M:%S'
class Site_Info:

    def __init__(self, target_dir, user:str):
        self.target_dir = target_dir
        self.user = user
        self.uuids = dict() # dict with keys: names values: uuids
        self.supported_directives = [{'name':'subjects', 'function': self.extract_subjects}, {'name':'tags', 'function': self.extract_tags}, {'name':'style', 'function': self.extract_style}]
        self.site_info = dict()
        self.get_site_info()

    def generate_ids(self, paths: list, id_tag: str, username: str, return_mapping: bool=False) -> list[str]:
        ids_paths: list[dict[str,str]] = [{ 'id': self.generate_id(username, id_tag), 'path': path } for path in paths]
        if return_mapping:
            return [ele['id'] for ele in ids_paths], ids_paths
        return [ele['id'] for ele in ids_paths]

    def get_site_info(self) -> dict():
        relationship_graph, data, index = self.build_site_info(self.target_dir)
        print(index)
        self.site_info = { "relationship_graph": relationship_graph, "data": data, "index": index}

    def create_note(self, id, path:Path):
        directive_data = self.extract_data(path.absolute())
        return {
            'id': id,
            'content': path.as_uri(),
            'subjects': directive_data['subjects'],
            'tags':directive_data['tags'],
            'metadata': self.note_metadata()
        }

    def node_metadata(self):
        """
        As you decide to add more metadata objects, return more objects from here
        """
        return {'timestamp': datetime.now().strftime(timestamp_format)}
    
    def note_metadata(self):
        """
        As you decide to add more metadata objects, return more objects from here
        """
        style = 'default' # TODO extract style from the file. It is a directive. use extract_style()
        return {'timestamp': datetime.now().strftime(timestamp_format),'style':style}

    def build_site_info(self, input_path) -> list[str]:

        def recurse_dirs(relationship_graph, data, index, blog_id: str, dir: Path):
            
            # is the root node getting recorded at all?
            # if not index['rootNode']:
            #     print('adding rootNode')
            #     index['rootNode']
            relationship_graph[blog_id] = {'blogs': [], 'notes': []}
            recursion_queue = []
            for f in dir.iterdir():
                if f.is_dir():
                    child_blog_id = self.generate_id(self.user, "blog")
                    index['blogs'].append(child_blog_id)
                    data['blogs'][child_blog_id] = {'name': f.name}
                    relationship_graph[blog_id]['blogs'].append(child_blog_id)
                    recursion_queue.append((child_blog_id,f))
                elif f.name.endswith('.md'):
                    id = self.generate_id(self.user, "note")
                    path = f.absolute()
                    relationship_graph[blog_id]['notes'].append(id)
                    index['notes'].append(id)
                    data['notes'].append(self.create_note(id, path))
            for blog_id,dir in recursion_queue:
                relationship_graph, data, index = recurse_dirs(relationship_graph, data, index, blog_id, dir)

            return relationship_graph, data, index

        root_id = self.generate_id(self.user, "blog")
        path = Path(input_path)
        return recurse_dirs(relationship_graph={}, data={"blogs": {root_id: {'name': path.name}}, "notes": []}, index={"blogs": [],"notes": [], "rootNode":root_id}, blog_id=root_id, dir=path)
    
    def generate_id(self, user, prefix: str) -> str:
        return f'{prefix}_{user}_{uuid.uuid4().hex[:5]}'

    def extract_data(self, filepath: str, ):
        with open(filepath, 'r') as f:
            contents = f.read()
        directive_data: dict[str: [str]] = self.get_directives(contents, filepath)
        return directive_data
        # TODO add support for directives that are commands
        # return self.execute_commands(directive_data)

    def get_directives(self, contents: str, filepath: str) -> dict[str, list[str]]:
        """
        At present, directive commands do not have context. They are simply pieces of text that are ignored by html
        """
        supported_directives = [s['name'] for s in self.supported_directives]
        directives = {directive:set() for directive in supported_directives}
        
        substr_start = 0

        directive_index = contents.find(directive_symbol_start, substr_start)
        while directive_index != -1:    
            colon_index = contents.find(':', directive_index)
            directive_end_index = contents.find(directive_symbol_end, colon_index)
            directive_start = directive_index + len(directive_symbol_start)
            directive: str = contents[directive_start:colon_index].strip(' ').lower()
            commands: list[str] = contents[colon_index+1:directive_end_index].split(',')
            commands = [command.strip(' ') for command in commands]
            # print(f'directive_command is {commands}')

            if directive not in supported_directives:
                print(f'{directive} is not a supported directive. Found {directive} in {filepath}')
            else:
                for command in commands:
                    directives.setdefault(directive, set()).add(command)
                    # else:
                    #     directives[directive] = set()
                    #     directives[directive].add(command)
                    
                    # print(f'directives: {directives}, command was {command}')
                    # directives.setdefault(directive, set()).add(command)

            substr_start = directive_end_index
            directive_index = contents.find(directive_symbol_start, substr_start)
        
        # we cannot write sets to json. This is a hacky solution to convert sets to lists
        for key in directives.keys():
                directives[key] = list(directives[key])
        print(f'directives: {directives}')
        return directives

    def execute_commands(self, found_directives: dict[str, list[str]]):
        results = {}
        self.supported_directives
        for supported_directive in self.supported_directives: # [{'name':'subjects', 'function': self.extract_subjects}, {'name':'tags', 'function': self.extract_tags}]
            if supported_directive['name'] in found_directives:
                commands = found_directives[supported_directive['name']]
                for command in commands:
                    results[supported_directive['name']] = supported_directive['function'](command)
        return results

    def extract_tags(self, tag):
        return tag

    def extract_subjects(self,subject):
        return subject

    def extract_style(self, style):
        return style

    # def extract_data(self, nextraction_functions: dict(str,list(Function))):
    #     # search for the symbol

    #     # goal: retrieve directives and their content

    #     #  return {{k, v(f)} for k,v in extraction_functions} # there is a method that yields the l and v of a single object here
    #     pass