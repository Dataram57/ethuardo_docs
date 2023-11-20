# Ethuardo Documentation

This is a simple static website generator designed to be an alternative to the gitbook. Designed to work with default NGINX or Apache.

## Demo

Working and commercial demo can be found here: [https://docs.ethuardo.com/](https://docs.ethuardo.com/)

# How to use?

## Baking

To bake `/docs/` into `/build/` use `python bake.py`. Simple HTTP server is up to.

## Writing /docs

- Markdown files (`.md`):
    - The title of a document is determined by the first H1 header.
- Hierarchy files (`.hierarchy`):
    - Defines how the specific folder should be rendered.
    - `# SECTION_NAME` - Writes section.
    - `FILE.md` - Links to a specific document.
    - `/ FOLDER_NAME` - Links to a specific folder.
    - `...` - Links to the rest of not mentioned files.
- `/img/` Folder is not being rendered, but it is copied.
