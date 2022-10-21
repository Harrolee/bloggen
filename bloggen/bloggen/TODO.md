# Bugs:

# How

Make the class that changes links a class that references the provider defined in a central config file

# Next

## Publish cleanup

accept no arguments

## Strategy for generating site_info

### data

the contents of site_info.data might change.
create a modular function that composes itself of provided functions. For example:

```
def build_siteinfo_data(extract_subject, extract_content, extract_tags, generate_metadata, generate_id, notes):
	return [{"id": generate_id(note), "subject": extract_subject(note), "content": extract_content(note), "tags": extract_tags(note), "metadata": generate_metadata(note)} for note in notes]
```

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
