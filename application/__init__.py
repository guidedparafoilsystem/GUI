from flask import Flask

app = Flask(__name__)
from application import views
from application.imap_gmail_script import main
