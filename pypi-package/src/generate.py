import os
from sys import stderr
import markdown
import bs4
from pathlib import Path, PurePath

def get_static_site_dir():
    dir = os.path.dirname(__file__)
    path = Path(dir)
    path = path.parent.absolute()
    path = path.joinpath('static-site')
    return path.absolute().as_posix()

def html_files(path_to_md_dir:str):
    not_md = []
    for md in os.listdir(path_to_md_dir):
        if md.endswith('.md'):
            print('file: '+ md)
            print(os.path.join(path_to_md_dir,md))
            __html_file(os.path.join(path_to_md_dir,md))
        else:
            not_md.append(md)
    if not_md:
        for file in not_md:
            print(f'{file} is not a markdown file')

def __html_file(path_to_md:str,outdir:str=os.path.join(get_static_site_dir(), 'notes')):
    """
    Converts a single markdown file to html and writes it to a given dir.
    """
    filename = os.path.basename(path_to_md).replace('.md','.html')
    outfile = os.path.join(outdir,filename)
    with open(path_to_md) as f:
            md_input = f.read()
    html = markdown.markdown(md_input)
    with open(outfile, 'x') as f:
        f.write(html)

def index(path_to_site:str=get_static_site_dir()):
    """
    Scans generated html files and creates links to them on the index.html page.
    for every html in ../notes dir of static site, add link to index
    """
    path_to_posts_dir = os.path.join(path_to_site,'notes')
    path_to_index = os.path.join(path_to_site,'index.html')
    with open('index.html') as in_f:
        txt = in_f.read()
        soup = bs4.BeautifulSoup(txt, features="html5lib")
    os.remove(path_to_index)
    post_names:list[str] = sorted(os.listdir(path_to_posts_dir))
    for post_name in post_names:
        new_li = soup.new_tag('li')
        new_anchor = soup.new_tag('a', href=os.path.join('notes',post_name))
        post_name = post_name.removesuffix('.html')
        new_anchor.attrs['id'] = post_name.replace(' ','')
        new_anchor.string = post_name
        new_li.append(new_anchor)
        soup.body.ul.append(new_li)

    with open(path_to_index, "x") as out_f:
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
        soup = bs4.BeautifulSoup(txt, features="html5lib")
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

def generate_site(path: str):
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
    pass