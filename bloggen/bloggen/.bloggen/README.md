## Do not remove files from .bloggen dir

## site.info

### Schema

- `index`: object containing the content of the site
  - `rootBlog`
  - `blogs`
  - `notes`
- `relationships`: describes the graph of blogs and notes
  - `[blog_uuid]`
    - `[childBlogs]`
    - `[childNotes]`
- `data`:
  - `[notes]`
    - `see (example)[example.site.info.json] for details`
  - `[nodes]`
    - `see (example)[example.site.info.json] for details`

#### sync strategy:

site.info is edited on every "sync" operation
^^ aka when the user saves their site
can save locally and globally

config file will need to reconcile itself against future versions
current plan:
newest config file wins
If we are pushing to a sink and we find a newer config file there,
opt.A: tell the user and show a diff of the two config files
opt.B: tell the user, save the older config as `old.config`, and keep the new config
