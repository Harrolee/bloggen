# Bugs:

### files in .bloggen dir

These should not contain my personal information.
Maybe they shouldn't even exist.
Up to you to implement/consider

# How

Make the class that changes links a class that references the provider defined in a central config file

# Next

## Publish cleanup

accept no arguments

## Stucture derivation

The user provides a notes directory.
Bloggen should derive the structure of the user's blog from the notes dir.
Bloggen should interpret every folder as a new blog node.

## Strategy for generating site_info

### data

the contents of site_info.data might change.
create a modular function that composes itself of provided functions. For example:

```
def build_siteinfo_data(extract_subject, extract_content, extract_tags, generate_metadata, generate_id, notes):
	return [{"id": generate_id(note), "subject": extract_subject(note), "content": extract_content(note), "tags": extract_tags(note), "metadata": generate_metadata(note)} for note in notes]
```

### relationships

bfs or dfs using os.scandir()
Learn why it's better to use one over the other

## How?

When user runs --generate, bloggen creates a site.info file

Steps:

- create index
- create relationship graph
- populate data

_These steps can happen in parallel_

### Potential pros of leaning in to it?

I could plop the template into the user's filesystem. Users could edit the template directly or make a copy of the template. Bloggen could import user-created templates, store them as `templates` in a json, and let the user add their template names to `"metadata":{template-style:"Kevin's Template"}`.

### What would I rather do?

Store the schema of the root template in json. Write a template-inflater to read the instructions of the json and generate the template when it is needed. Allow users to create their own templates with json.

### Why would I rather do it?

I want to write a dsl. I want to say that my app uses a dsl. I want to say that I have written a dsl.

## What implementation do both approaches share?

Bloggen imports template. bs4 imports html. bs4 imports and edits html according to defined user parameters.

##

```
Bloggen:

As notes:
-> phase 1:
	deployment tool
		-> support for multiple configurations
			eg buckets, platforms
			a local config file: a json that stores data for each configuration
				data is:

		-> users might want to create distinct clusters of notes
			- create an abstract structure for note-sets. Make this a structure nest-able
-> phase 2:
	associate notes with one another
		1. Tags, preceded by a specific symbol, in the footer of the file
		2. Explicit links, in the footer of the file —> use Andy M’s janitor tool to insert backlinks. format: [[ ]]
-> phase 3:
	enhance note-reading experience:
		load and render linked notes as pop-up boxes, like on Andy M’s site: https://notes.andymatuschak.org/About_these_notes
-> phase 4:
	enhance note-taking feature set


As blog:
-> phase 1:
	style presets for each note
		-> this makes blogger versatile:
			1. Posts for people to see, read, and follow
			2. Understand subject in a context of a the given note
				1. some notes will be graphs that show relationships of ideas
				2. Some notes with be short essays
				3. Some notes will compare images
				4. Some notes will associate images with text
				5. Some notes are todo lists
-> phase 2:
	IoC: let users associate js with their notes
	- maybe even with note structures?
```

## Lee:

push to testpypi:

1. build the new version:
   `poetry build`
2. publish:
   `poetry publish -r testpypi -u harolee -p`

pull from testpypi:
`pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple bloggen`
