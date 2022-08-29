from pathlib import PurePath
import os
import uuid

class site_info:

    def __init__(self, target_dir, user:str):
        self.target_dir = target_dir
        self.index = dict()
        self.relationships = dict()
        self.data = dict()
        self.user = user
        self.uuids = dict() # dict with keys: names values: uuids

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
        # `notes` contains list of note ids
        notes = self.__get_filenames(target_dir)
        self.index.update({"rootNode":rootNode},{"nodes":nodes},{"notes":notes})

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
        # nodes:
        node_ids = [{node: self.generate_id(user, "blog")} for node in index['nodes']]
        # - populate data for all elements
        ids_nodenames = [{self.generate_id(user, "note"): node } for node in index['notes']]
        noteid_subjects = [{note_id.keys(): self.extract_subjects()} for note_id in ids_nodenames]
        noteid_contents = False # get path to note
        noteid_tags = [{note_id.keys(): self.extract_tags()} for note_id in ids_nodenames]
        noteid_metadata = [{note_id.keys(): self.generate_metadata()} for note_id in ids_nodenames]

        pass

    def __get_sub_directories(self, dir_name) -> list[str]:
        sub_dirs = [f.name for f in os.scandir(dir_name) if f.is_dir()]
        for dir_name in list(sub_dirs):
            sub_dirs.extend(self.get_sub_directories(dir_name))
        return sub_dirs
    
    def __get_filenames(self, dir_name) -> list[str]:
        sub_files = [f.name for f in os.scandir(dir_name) if f.is_file()]
        for dir_name in list(sub_files):
            sub_files.extend(self.__get_filenames(dir_name))
        return sub_files
    
    def generate_id(user, prefix: str) -> str:
        return f'{prefix}_{user}_{uuid.uuid4().hex[:5]}'

    def extract_subjects():
        pass

    def extract_tags():
        pass

    def generate_metadata():
        pass