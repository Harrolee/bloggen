# Bloggen

Point bloggen to a hosting location, give it your markdown, then watch it deploy a static site.

# Use

## A parable:

Lee creates a GCP credentials json:

1.  Lee gets a service token JSON from GCP. He follows this guide https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication'
2.  Lee saves the JSON to his machine and remembers the path for later. Bloggen is going to save the path to that JSON into an environment variable
3.  Lee will need to tell Bloggen the path to the json by configuring a Bloggen profile

Lee configures a profile:

1. Lee runs `bloggen --config` and supplies the following information:

   - Name
   - Path to GCP credentials json
   - Name of GCP bucket to use

1. Lee writes 5 md notes into a dir
1. Lee runs `bloggen --generate path_to_md_dir`
1. Lee sees a new dir appear. It is named static-site and can be found at ../path_to_md_dir
1. Lee runs `bloggen --publish path_to_static_site`
1. Lee learns that his notes are available as a static site on GCP

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
