import os
from sys import stderr, exit
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

def html_files(input_dir:Path, output_dir:Path):
    not_md = []
    for path in Path.iterdir(input_dir):
        filename = path.name
        if filename.endswith('.md'):
            print('file: '+ filename)
            __html_file(Path.joinpath(input_dir,filename), Path.joinpath(output_dir, 'notes'))
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
    outfile = Path.joinpath(output_dir,filename)
    with open(input_file) as f:
            md_input = f.read()
    html = markdown.markdown(md_input)
    with open(outfile, 'w') as f:
        f.write(html)

def index(path_to_site):
    """
    Scans generated html files and creates links to them on the index.html page.
    For every html in ../notes dir of static site, add link to index
    This function assumes that there are notes in the ../static-site/notes dir
    """
    path_to_posts_dir = Path.joinpath(path_to_site,'notes')
    path_to_index = Path.joinpath(path_to_site,'index.html')
    with open(path_to_index) as in_f:
        txt = in_f.read()
        soup = bs4.BeautifulSoup(txt, features="html.parser")
    post_names:list[str] = sorted([note.name for note in Path.iterdir(path_to_posts_dir)])
    for post_name in post_names:
        new_li = soup.new_tag('li')
        new_anchor = soup.new_tag('a', href=os.path.join('notes',post_name))
        post_name = post_name.removesuffix('.html')
        new_anchor.attrs['id'] = post_name.replace(' ','')
        new_anchor.string = post_name
        new_li.append(new_anchor)
        soup.body.ul.append(new_li)
    with open(path_to_index, "w") as out_f:
        out_f.write(str(soup))

def prep_for_hosting(notes_root:str, ):
    # access config file
    switch_index_references(notes_root)

# Please refactor to take a callback. Follow this guide: # https://stackoverflow.com/questions/55751368/python-how-to-pass-to-a-function-argument-type-of-a-class-object-typing
def switch_index_references(notes_root:str,path_to_site:str=get_static_site_dir()):
    path_to_posts_dir = os.path.join(path_to_site,'notes')
    path_to_index = os.path.join(path_to_site,'index.html')
    with open(path_to_index) as in_f:
        txt = in_f.read()
        soup = bs4.BeautifulSoup(txt, features="html.parser")
    os.remove(path_to_index)
    post_names:list[str] = sorted(os.listdir(path_to_posts_dir))
    for post_name in post_names:
        tag_id = post_name.removesuffix('.html').replace(' ','')
        anchor:bs4.Tag = soup.find(id=tag_id)
        if anchor:
            anchor.attrs['href'] = notes_root + post_name.replace(' ','%20')
        else:
            print(f"Index.html linking won't work. Could not find a tag with tag_id '{tag_id}'. As a result, I could not update the link.",stderr)

    with open(path_to_index, "x") as out_f:
        out_f.write(str(soup))    

def static_site(static_site_root: Path):
    """
    later --> Have object of static site in memory
    1. Generate static site directory structure
        1a. create index.html file
        1b. Create open html tags
    2. for very md file in folder, convert to html
        2a. write to a file in notes dir
        2b. add link of each file to open html tag in index.html
    3. 
    """
    if Path.exists(static_site_root):
        print(f'static-site dir already exists at ${static_site_root}. Canceling generation.')
        exit()
    
    # make dirs
    os.mkdir(static_site_root)
    os.mkdir(Path.joinpath(static_site_root, 'notes'))
    os.mkdir(Path.joinpath(static_site_root, 'data'))
    os.mkdir(Path.joinpath(static_site_root, 'scripts'))

    with open(Path.joinpath(static_site_root, 'robots.txt'), 'w+') as f:
        f.writelines(['User-agent: *\n','Disallow: /'])
    reference_index_path = Path.joinpath(pathlib.Path(__file__).parent, '.bloggen/index.html')
    shutil.copy(reference_index_path,Path.joinpath(static_site_root, 'index.html'))