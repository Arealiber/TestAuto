import os

from flask import Flask

from application.config import default


web_root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(web_root, 'templates'))
)
app.config.from_object(default)
