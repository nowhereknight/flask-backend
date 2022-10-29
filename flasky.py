import os
import sys
import click
from app import create_app, db
from app.models import Company

app = create_app(os.getenv('FLASK_CONFIG') or 'default')