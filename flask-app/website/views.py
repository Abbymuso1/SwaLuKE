from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Translation, User_Translation
#from .model_handler import translate_text
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from . import db
import json

views = Blueprint('views', __name__)

model_name = "AbbyMuso1/model_trans_lu_sw_3"  # Replace with your model name
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


#define views
@views.route('/', methods=['GET', 'POST']) #main page of the website
#@login_required
def home():
    if request.method == 'POST':
        original_text = request.form.get('original_text')
        inputs = tokenizer.encode("translate Luhya to Swahili: " + original_text, return_tensors="pt")
        translation = model.generate(inputs, max_length=90, num_return_sequences=1)
        translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
        
        if translated_text:
            new_translation = Translation(original_text=original_text, translated_text=translated_text)
            db.session.add(new_translation)
            db.session.commit()
            flash('Translation Added!', category='success')
            render_template("newbase.html", user=current_user,new_translation=new_translation)
        

    return render_template("newbase.html", user=current_user)


@views.route('/translate', methods=['GET', 'POST'])
def translate():
    original_text = "si ndareta"
    inputs = tokenizer.encode("translate Luhya to Swahili: " + original_text, return_tensors="pt")
    translation = model.generate(inputs, max_length=90, num_return_sequences=1)
    translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
    
    data = Translation.query.all()
    return render_template('index.html', original_text=original_text, translated_text=translated_text, data=data)


@views.route('/delete-note', methods= ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})


@views.route('/translation', methods=['GET', 'POST']) #main page of the website
@login_required
def translation_page():
    if request.method == 'POST':
        source_text = request.form.get('source_text')
        translated_text = request.form.get('translated_text')
        if len(source_text) < 1:
            flash('Input text is too short!', category='error')
        else:
            new_translation = Translation(source_text=source_text, translated_text=translated_text, user_id=current_user.id)
            db.session.add(new_translation)
            db.session.commit()
            flash('Translation Added!', category='success')

    return render_template("translation.html", user=current_user)

@views.route('/delete-translation', methods= ['POST'])
def delete_translation():
    translation = json.loads(request.data)
    transId = translation['transId']
    translation = Translation.query.get(transId)
    if translation:
        if translation.user_id == current_user.id:
            db.session.delete(translation)
            db.session.commit()
    
    return jsonify({})


@views.route('/dashboard', methods=['GET', 'POST']) #main page of the website
@login_required
def dashboard():
    return render_template("userdashboard.html", user=current_user, usertrans=User_Translation)

@views.route('/addtranslation', methods=['GET', 'POST']) #main page of the website
@login_required
def addtranslation():
    return render_template("add_translation.html", user=current_user)

@views.route('/viewaddtranslation', methods=['GET', 'POST']) #main page of the website
@login_required
def viewaddtranslation():
    return render_template("view_add_translation.html", user=current_user)

@views.route('/userprofile', methods=['GET', 'POST']) #main page of the website
@login_required
def userprofile():
    return render_template("user_profile.html", user=current_user)

@views.route('/translation', methods=['GET', 'POST']) #main page of the website
@login_required
def translation():
    return render_template("translation.html", user=current_user)

    