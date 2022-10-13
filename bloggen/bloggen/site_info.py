from io import TextIOWrapper
from pathlib import PurePath
import os
from typing import Dict, List
import uuid

directive_symbol_start = '$-<<'
directive_symbol_end = '>>-$'

class Site_Info:

    def __init__(self, target_dir, user:str):
        self.target_dir = target_dir
        self.index = dict()
        self.relationships = dict()
        self.data = dict()
        self.user = user
        self.uuids = dict() # dict with keys: names values: uuids
        self.supported_directives = [{'name':'subjects', 'function': self.extract_subjects}, {'name':'tags', 'function': self.extract_tags}]
        self.get_site_info()

    def get_site_info(self) -> dict():
        self.__create_index(self.target_dir)
        # orchestrate the below
        self.find_relationships()
        # return a site_info dict
        self.create_data(self.user, self.index)
        pass

    def __create_index(self, target_dir):
        """
        index is a list of contents.
        index is not a record of relationships.
        """
        # root node is the highest dir
        rootNode = PurePath(target_dir).name
        # `nodes` contains list the dirs present in the dir heirarchy
        nodes = self.__get_sub_directories(target_dir)
        print(nodes)
        # `notes` contains list of note ids
        notes = self.__get_filenames(target_dir)
        filepaths = self.__get_filepaths(target_dir)
        self.index.update({"rootNode":rootNode})
        self.index.update({"nodes":nodes})
        self.index.update({"notes":notes})

    def find_relationships(self):
        """
        consider either bfs or dfs for this task
        use os.scandir() and __get_sub_directories() as an example
        """
        # - create relationship graph
        pass

    def create_data(self, user, index):
        """
        For all nodes, generate an id and a metadata field.
        For all notes, generate an entry as listed in the example.site.info.json
        """
        # nodes: THis is a list of dictionaries: key=nodeName, value=uuid
        node_ids = [{node: self.generate_id(user, "blog")} for node in index['nodes']]
        print('I hope these are dirs')
        print(node_ids)
        # - populate data for all elements
        ids_nodenames = [{self.generate_id(user, "note"): node } for node in index['notes']]
        print('these seem to be notes')
        print(ids_nodenames)
        # what do I do with the subjects and tags after I have them?
        # 

        # need the path to the note
        # consider passing the path into the index object or into the create_data method directly
        #data = self.extract_data()
             
             #[{note_id.keys(): for note_id in ids_nodenames]
        # perform these two in the same r/w operation:
        # noteid_subjects = [{note_id.keys(): self.extract_subjects()} for note_id in ids_nodenames]
        # noteid_tags = [{note_id.keys(): self.extract_tags()} for note_id in ids_nodenames]
        # # put the above in this function:
        # #extract_data()

        # noteid_metadata = [{note_id.keys(): self.generate_metadata()} for note_id in ids_nodenames]
        # noteid_contents = False # get path to note

        pass

    def __get_sub_directories(self, dir_name) -> list[str]:
        sub_dirs = [f.name for f in os.scandir(dir_name) if f.is_dir()]
        # what was I after with the below code?
        # for dir_name in sub_dirs:
        #     sub_dirs.extend(self.__get_sub_directories(dir_name))
        return sub_dirs
    
    def __get_filenames(self, dir_name) -> list[str]:
        # at this point, there cannot be any non md files in this dir
        # alternatively, find a way to grab only the md files
        sub_files = [f.name for f in os.scandir(dir_name) if f.is_file()]
        print(sub_files)
        # for dir_name in sub_files:
        #     sub_files.extend(self.__get_filenames(dir_name))
        return sub_files
    
    def __get_filepaths(self, dir_name) -> list[str]:
        # at this point, there cannot be any non md files in this dir
        # alternatively, find a way to grab only the md files
        sub_files = [f.path for f in os.scandir(dir_name) if f.is_file()]
        print(f'paths to files are: {sub_files}')
        # for dir_name in sub_files:
        #     sub_files.extend(self.__get_filenames(dir_name))
        return sub_files
    
    def generate_id(self, user, prefix: str) -> str:
        return f'{prefix}_{user}_{uuid.uuid4().hex[:5]}'

    def extract_subjects(self,):
        pass

    def extract_tags(self,):
        pass

    def generate_metadata(self,):
        pass


    def extract_data(self, filepath: str, ):
        with open(filepath, 'r') as f:
            contents = f.read()
        directives: Dict[str: [str]] = self.get_directives(contents)
        self.validate_directives(directives, filepath)
        
        # self.extract_tags(directives['tags'])
        # self.extract_subjects(directives['subjects'])

        return self.execute_commands(directives)

    def validate_directives(self,directives, filepath):
        supported_directives = [s['name'] for s in self.supported_directives]
        for directive in directives:
            if directive not in supported_directives:
                print(f'{directive} is not a supported directive. Found {directive} in {filepath}')
                directive.pop

    def get_directives(self, contents: str) -> Dict[str, List[str]]:
        directives = {}

        substr_start = 0
        directive_index = contents.find(directive_symbol_start, substr_start)
        while directive_index:    
            colon_index = contents.find(':', directive_index)
            directive_end_index = contents.find(directive_symbol_end, colon_index)

            directive: str = contents[directive_index:colon_index]
            directive_command: str = contents[colon_index:directive_end_index]
            directives.setdefault(directive, []).append(directive_command)
            
            substr_start = directive_end_index
            directive_index = contents.find(directive_symbol_start, substr_start)
            
        return directives

    def execute_commands(self, found_directives: Dict[str, List[str]]):
        results = {}
        for supported_directive in self.supported_directives: # [{'name':'subjects', 'function': self.extract_subjects}, {'name':'tags', 'function': self.extract_tags}]
            if supported_directive['name'] in found_directives:
                commands = found_directives[supported_directive['name']]
                for command in commands:
                    results[supported_directive['name']] = supported_directive['function'](command)
        return results



    # def extract_data(self, nextraction_functions: Dict(str,List(Function))):
    #     # search for the symbol

    #     # goal: retrieve directives and their content

    #     #  return {{k, v(f)} for k,v in extraction_functions} # there is a method that yields the l and v of a single object here
    #     pass