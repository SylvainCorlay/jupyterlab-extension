"""Tornado handlers for the Lab view."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from tornado import web
from notebook.base.handlers import IPythonHandler, FileFindHandler
from jinja2 import ChoiceLoader, FileSystemLoader, FunctionLoader


FILE_LOADER = FileSystemLoader(os.path.dirname(__file__))
PREFIX = '/lab'
app = None

class LabHandler(IPythonHandler):
    """Render the Jupyter Lab View."""   

    @web.authenticated
    def get(self):
        self.write(self.render_template('lab.html',
            static_prefix=PREFIX,
            page_title='Pre-Alpha Jupyter Lab Demo',
            terminals_available=self.settings['terminals_available'],
            mathjax_url=self.mathjax_url,
            mathjax_config='TeX-AMS_HTML-full,Safe',
            #mathjax_config=self.mathjax_config # for the next release of the notebook
        ))

    def get_template(self, name):
        return FILE_LOADER.load(self.settings['jinja2_env'], name)

#-----------------------------------------------------------------------------
# URL to handler mappings
#-----------------------------------------------------------------------------

default_handlers = [
    (PREFIX, LabHandler),
    (PREFIX+r"/(.*)", FileFindHandler,
        {'path': os.path.join(os.path.dirname(__file__), 'build')}),
    ]

def _jupyter_server_extension_paths():
    return [{
        "module": "jupyterlab_extension"
    }]
    
def load_jupyter_server_extension(nbapp):
    nbapp.log.info('Pre-alpha version of Lab extension loaded')
    global app
    app = nbapp

    webapp = nbapp.web_app
    #base_url = webapp.settings['base_url']
    webapp.add_handlers(".*$", default_handlers)
