from datetime import datetime
from pathlib import PurePath
import os
from typing import Dict, List
import uuid

directive_symbol_start = '<!--$'
directive_symbol_end = '$-->'

class Site_Info:

    def __init__(self, target_dir, user:str):
        self.target_dir = target_dir
        self.index = dict()
        self.relationships = dict()
        self.data = dict()
        self.user = user
        self.uuids = dict() # dict with keys: names values: uuids
        self.supported_directives = [{'name':'subjects', 'function': self.extract_subjects}, {'name':'tags', 'function': self.extract_tags}, {'name':'style', 'function': self.extract_style}]
        self.get_site_info()

    def get_site_info(self) -> dict():
        note_paths = self.__get_filepaths(self.target_dir)
        noteIds_notepaths: List[Dict[str,str]] = [{ 'id': self.generate_id(self.user, "note"), 'path': path } for path in note_paths]
        note_ids = [ele['id'] for ele in noteIds_notepaths]
        
        # index object
        self.__create_index(self.target_dir, note_ids)
        # TODO rootnode and nodes list should contain node ids, not folder names
        print(self.index)

        # relationship object
        # TODO
        self.find_relationships()

        # return a site_info dict
        self.create_data(self.user, self.index, noteIds_notepaths)
        print(self.data)

    def __create_index(self, target_dir, note_ids: List[str]):
        """
        index is a list of contents.
        index is not a record of relationships.
        """
        # root node is the highest dir
        rootNode = PurePath(target_dir).name
        # `nodes` contains list the dirs present in the dir heirarchy
        nodes = self.__get_sub_directories(target_dir)

        # filepaths = self.__get_filepaths(target_dir)
        self.index.update({"rootNode":rootNode})
        self.index.update({"nodes":nodes})
        self.index.update({"notes":note_ids})

    def find_relationships(self):
        """
        consider either bfs or dfs for this task
        use os.scandir() and __get_sub_directories() as an example
        """
        # - create relationship graph
        pass



    def create_data(self, user, index, noteIds_notepaths):
        """
        For all nodes, generate an id and a metadata field.
        For all notes, generate an entry as listed in the example.site.info.json
        """
        nodes = [{node: self.generate_id(user, "blog"), 'metadata': [self.node_metadata()]} for node in index['nodes']]
        notes = [self.create_note(noteId_notepath) for noteId_notepath in noteIds_notepaths]
        self.data['nodes'] = nodes
        self.data['notes'] = notes

    def create_note(self, noteId_notepath: Dict[str,str]):
        id = noteId_notepath['id']
        path = noteId_notepath['path']
        directive_data = self.extract_data(path)
        print(f'directive_data is: {directive_data}')
        # TODO account for directive data being empty AKA user did not write a directive for tags or for subjects
        return {
            'id': id,
            'content': path,
            'subjects': directive_data['subjects'],
            'tags':directive_data['tags'],
            'metadata': self.note_metadata(path)
        }

    def node_metadata(self):
        """
        As you decide to add more metadata objects, return more objects from here
        """
        return {'timestamp': datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
    
    def note_metadata(self, path):
        """
        As you decide to add more metadata objects, return more objects from here
        """
        style = 'default' # TODO extract style from the file. It is a directive. use extract_style()
        return {'timestamp': datetime.now().strftime("%Y/%m/%dT%H:%M:%S")}, {'style':style}

    def __get_sub_directories(self, dir_name) -> list[str]:
        sub_dirs = [f.name for f in os.scandir(dir_name) if f.is_dir()]
        # what was I after with the below code?
        # for dir_name in sub_dirs:
        #     sub_dirs.extend(self.__get_sub_directories(dir_name))
        return sub_dirs
    
    def __get_filepaths(self, dir_name) -> list[str]:
        sub_files = [f.path for f in os.scandir(dir_name) if f.is_file() and f.name.endswith('.md') ]
        return sub_files
    
    def generate_id(self, user, prefix: str) -> str:
        return f'{prefix}_{user}_{uuid.uuid4().hex[:5]}'

    def extract_data(self, filepath: str, ):
        with open(filepath, 'r') as f:
            contents = f.read()
        directive_data: Dict[str: [str]] = self.get_directives(contents, filepath)
        return directive_data
        # TODO add support for directives that are commands
        #return self.execute_commands(directives)

    def get_directives(self, contents: str, filepath: str) -> Dict[str, List[str]]:
        """
        At present, directive commands do not have context. They are simply pieces of text that are ignored by html
        """
        directives = {}
        supported_directives = [s['name'] for s in self.supported_directives]
        substr_start = 0

        directive_index = contents.find(directive_symbol_start, substr_start)
        print(f'directive_index: {directive_index}')
        while directive_index != -1:    
            colon_index = contents.find(':', directive_index)
            print(f'colon_index: {colon_index}')
            directive_end_index = contents.find(directive_symbol_end, colon_index)
            directive_start = directive_index + len(directive_symbol_start)
            directive: str = contents[directive_start:colon_index].strip(' ').lower()
            directive_command: str = contents[colon_index+1:directive_end_index].strip(' ').split(',')

            if directive not in supported_directives:
                print(f'{directive} is not a supported directive. Found {directive} in {filepath}')
            else:
                for command in directive_command:
                    directives.setdefault(directive, set()).add(command)

            substr_start = directive_end_index
            directive_index = contents.find(directive_symbol_start, substr_start)

        return directives

    def execute_commands(self, found_directives: Dict[str, List[str]]):
        results = {}
        for supported_directive in self.supported_directives: # [{'name':'subjects', 'function': self.extract_subjects}, {'name':'tags', 'function': self.extract_tags}]
            print(f'found these directives: {found_directives}')
            if supported_directive['name'] in found_directives:
                commands = found_directives[supported_directive['name']]
                print(f'commands are: {commands}')
                for command in commands:
                    results[supported_directive['name']] = supported_directive['function'](command)
        return results

    def extract_tags(self, tag):
        return tag

    def extract_subjects(self,subject):
        return subject

    def extract_style(self, style):
        return style

    # def extract_data(self, nextraction_functions: Dict(str,List(Function))):
    #     # search for the symbol

    #     # goal: retrieve directives and their content

    #     #  return {{k, v(f)} for k,v in extraction_functions} # there is a method that yields the l and v of a single object here
    #     pass