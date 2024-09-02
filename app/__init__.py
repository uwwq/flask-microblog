import os
from flask import Flask
import config

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

template_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.config.from_object(config)

from app import models, views, api
