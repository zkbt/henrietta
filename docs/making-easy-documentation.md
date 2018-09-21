# How do I set up sphinx documentation?
(written by zkbt on 9/21/18)

Run `sphinx-quickstart` and answer a series of questions. This will create
an empty template documentation page. You can then add source materials to
the `source` directory. The most intuitive way I've found for doing this is
to use ipython notebooks as the sources. To build the source into a viewable
set of documentaion, you can then run (for example) `make html` to populate
`build/html` with HTML pages built from the source. I then copy those to another
directory and post them manually to a github-pages space, but I'm sure there's
also a way of automating that process.

To be able to push to a github-page, include 'sphinx.ext.githubpages' in the
`extensions` list inside `conf.py`. To be able to include `.ipynb` notebooks
as documentation pages, be sure to include 'nbsphinx' in the `extensions` too.
If you don't want sphinx to automatically run your notebooks (leaving them
blank keeps them smaller if you're going to keep pushing them to a repository),
then set `nbsphinx_execute = 'never'` in `conf.py`.
