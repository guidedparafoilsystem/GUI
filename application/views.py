from application import app
from flask import render_template
from flask import jsonify
from application.imap_gmail_script import main

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
                            
@app.route('/update')
def update():
    return jsonify(main())
    
                            