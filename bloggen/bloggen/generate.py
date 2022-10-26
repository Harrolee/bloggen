import json
import os
from pyclbr import Function
from sys import stderr, exit
from typing import Dict
import markdown
import bs4
from pathlib import Path
import shutil
import pathlib

    # gets the dir of static-site if it is the same dir as bloggen itself.
def get_static_site_dir():
    dir = os.path.dirname(__file__)
    path = Path(dir)
    path = path.parent.absolute()
    path = path.joinpath('static-site')
    return path.absolute().as_posix()

def blog_structure(output_path, site_info):
    def recurse(parent_blog_id, output_path):
        for blog_id in site_info['relationship_graph'][parent_blog_id]['blogs']:
            blog_name = site_info['data']['blogs'][blog_id]['name']
            blog_dir = Path.joinpath(output_path, blog_name)
            os.mkdir(blog_dir)
            recurse(blog_id, blog_dir)
    
    root_blog_id = site_info['index']['rootNode']
    blog_name = site_info['data']['blogs'][root_blog_id]['name']
    blog_dir = Path.joinpath(output_path, blog_name)
    os.mkdir(blog_dir)
    recurse(root_blog_id, blog_dir)

def blog_notes(input_path:Path, output_root_dir):
    #TODO find a way to put the first node in the while loop before
    output_path = Path.joinpath(output_root_dir, input_path.name)
    html_files(input_path, output_path)
    input_path_queue = [(input_path, output_path)]
    
    while len(input_path_queue) > 0:
        input_path, output_path = input_path_queue.pop()
        input_subdirs = [x for x in input_path.iterdir() if x.is_dir()]
        subdirs_that_are_parents = [x for x in input_subdirs if has_children(x)]
        for child in subdirs_that_are_parents:
            output_path = Path.joinpath(output_path,child.name)
            html_files(child, output_path)
            input_path_queue.append((child, output_path))

    
def has_children(dir: Path):
    children = [x for x in dir.iterdir()]
    if len(children) > 0:
        return True
    return False

def html_files(input_dir:Path, output_dir:Path):
    not_md = []
    for file in Path.iterdir(input_dir):
        filename = file.name
        if filename.endswith('.md'):
            print('adding note: '+ filename)
            __html_file(Path.joinpath(input_dir,filename), output_dir)
        else:
            not_md.append(filename)
    if not_md:
        for file in not_md:
            print(f'{file} is not a markdown file')

def __html_file(input_file:str,output_dir:Path):
    """
    Converts a single markdown file to html and writes it to a given dir.
    """
    filename = os.path.basename(input_file).replace('.md','.html')
    print(f'filename is {filename}')
    outfile = Path.joinpath(output_dir,filename)
    with open(input_file) as f:
            md_input = f.read()
    html = markdown.markdown(md_input)
    with open(outfile, 'w') as f:
        f.write(html)

def index_html(path_to_site: Path, root_blog_name):
    cook_soup(path_to_site, root_blog_name, recipe=index_md_files, ingredients={'blog_root': root_blog_name})

def prep_for_hosting(path_to_static_site:Path, root_blog_name:str, ):
    # we need to get the dir names into the ingredients variable
    cook_soup(path_to_static_site, root_blog_name, prep_for_cloud, ingredients={'blog_root': root_blog_name})

def cook_soup(path_to_site: Path, root_blog_name, recipe:Function, ingredients:Dict={}):
    """
    Create a soup from the index file.
    Retrieve the names of every note.
    Apply a given recipe to the soup.
    """
    path_to_posts_dir = Path.joinpath(path_to_site,root_blog_name)
    path_to_index = Path.joinpath(path_to_site,'index.html')
    with open(path_to_index) as in_f:
        txt = in_f.read()
        soup = bs4.BeautifulSoup(txt, features="html.parser")
    note_names:list[str] = sorted([note.name for note in Path.iterdir(path_to_posts_dir)])
    for note_name in note_names:
        ingredients['post_name'] = note_name
        recipe(ingredients, soup)
    with open(path_to_index, "w") as out_f:
        out_f.write(str(soup))  

def index_md_files(data:dict, soup):
    """
    Scans generated html files and creates links to them on the index.html page.
    For every html in blog root of static site, add link to index
    This function assumes that there are notes in the ../static-site/{blog_root}
    """
    post_name = data['post_name']
    blog_root = data['blog_root']
    new_li = soup.new_tag('li')
    new_anchor = soup.new_tag('a', href=os.path.join(blog_root,post_name))
    post_name = post_name.removesuffix('.html')
    new_anchor.attrs['id'] = post_name.replace(' ','')
    new_anchor.string = post_name
    new_li.append(new_anchor)
    soup.body.ul.append(new_li)

def prep_for_cloud(data:dict, soup):
    """
    Change anchor hrefs so that they use relative paths instead of absolute filepaths.
    """
    post_name = data['post_name']
    blog_root = data['blog_root']
    tag_id = post_name.removesuffix('.html').replace(' ','')
    anchor:bs4.Tag = soup.find(id=tag_id)
    if anchor:
        anchor.attrs['href'] = f"{blog_root}/{ post_name.replace(' ','%20') }"
    else:
        print(f"Index.html linking won't work. Could not find a tag with tag_id '{tag_id}'. As a result, I could not update the link.",stderr)

def static_site_structure(static_site_root: Path, site_info: Dict):
    """
    1. Generate static site directory structure
        1a. create index.html file
        1b. Create open html tags
    2. for very md file in folder, convert to html
        2a. write to a file in notes dir
        2b. add link of each file to open html tag in index.html
    """
    if Path.exists(static_site_root):
        print(f'static-site dir already exists at ${static_site_root}. Canceling generation.')
        exit()

    os.mkdir(static_site_root)
    os.mkdir(Path.joinpath(static_site_root, 'data'))
    os.mkdir(Path.joinpath(static_site_root, 'scripts'))

    with open(Path.joinpath(static_site_root, 'robots.txt'), 'w+') as f:
        f.writelines(['User-agent: *\n','Disallow: /'])
    
    # create index.html file
    reference_index_path = Path.joinpath(pathlib.Path(__file__).parent, '.bloggen/index.html')
    shutil.copy(reference_index_path,Path.joinpath(static_site_root, 'index.html'))

    f = open(Path.joinpath(static_site_root, 'data/site_info.json'), 'w+')
    json.dump(site_info, f)
    f.close()