# Main functions

#---[Libraries]-----------------------------------------------------------------
from flask import * # imports libraries for flask web development
import os
import smtplib
from functions import *
import requests
import json
from pprint import pprint
from werkzeug.utils import secure_filename
#---[File import code and storage]----------------------------------------------
UPLOAD_FOLDER = 'static/imaging'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#-------------------------------------------------------------------------------
#-------------------------[MAIN APPLICATION]------------------------------------
#-------------------------------------------------------------------------------

#---[App configuration]---------------------------------------------------------

app = Flask(__name__) # initializes app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class cloud():
    voice = ''
    pic = ''
    places = {
        0 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        1 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        2 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        3 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        4 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        5 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        6 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        7 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        8 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" },
        9 : { "name" : "" , "rating" : "" , "address" : "" , "website" : "" , "number" : "" }
    }
x = cloud()
    
#---[Homepage]------------------------------------------------------------------
@app.route ('/')
def homepage():
    return render_template('home.html')

#---[Voice Recognition]---------------------------------------------------------    
@app.route('/voice')
def voice_rec():
    return render_template('voice.html', text=x.voice)

@app.route('/voice', methods=["POST"])
def voice_res():
    source = request.form['source']
    print source
    target = request.form['target']
    print target
    text = request.form['user_input']
    print text
    x.voice = translate(source, target, text)
    return redirect(url_for('voice_rec'))

#---[Character recognition and Translator]--------------------------------------
@app.route('/pic')
def pic_rec():
    return render_template('pic.html', text=x.pic)

@app.route('/pic', methods=["POST"])
def export_txt():
    target = request.form['target']
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = picture(filename)
        detected = data['lang']
        text = data['words']
        x.pic = translate(detected, target, text)
        os.remove('static/imaging/' + filename)
        return redirect(url_for('pic_rec'))


#---[Nearby Places]-------------------------------------------------------------
@app.route('/places')
def places():
    params = x.places
    return render_template('places.html', params=params)

@app.route('/places', methods = ["POST"])
def place_search():
    query_search = request.form['query_search']
    search_places(query_search, x.places)
    return redirect(url_for('places'))
#---[Server Identity Checker]---------------------------------------------------
if __name__ == '__main__':
    app.run(
        port=int(os.getenv('PORT', 8080)),
        host=os.getenv("IP", "0.0.0.0"),
        debug=True
        )