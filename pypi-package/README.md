# Bloggen

Point bloggen to a hosting location, give it your markdown, then watch it deploy a static site.

# Setup

1. copy sample.env as .env
1. put config variables in sample.env

# Use

## Generate

_generates static webpage_
User provides a directory of markdown to be converted to html

`bloggen generate --path=path_to_dir`

## Sync

_Sync directory of markdown files with existing static site_
`bloggen sync --path=path_to_dir_of_md_files`

## Add

_Add file to static site_
_Convert given markdown file to html and add to site_
`bloggen add --path=path_to_md_file`

## Remove

_Remove named page from static site_
`bloggen remove --name=name_of_file`

## Destroy

_Destroy site and bucket_
`bloggen destroy`
