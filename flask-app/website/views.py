from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Translation, Feedback
#from .model_handler import translate_text
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from . import db
import json

views = Blueprint('views', __name__)

model_name = "AbbyMuso1/model_trans_lu_sw_3"  # Replace with your model name
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
translator = pipeline(task="translation", model=model, tokenizer=tokenizer)


#define views
@views.route('/', methods=['GET', 'POST']) #main page of the website
#@login_required
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        if len(message) < 1:
            flash('Input text is too short!', category='error')
        else:
            new_feedback = Feedback(name=name, email=email, subject=subject, message=message)
            db.session.add(new_feedback)
            db.session.commit()
            flash('Feedback Added!', category='success')

    return render_template("newbase.html", user=current_user )


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
    return render_template("userdashboard.html", user=current_user)

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

@views.route('/translate', methods=['GET', 'POST'])
def translate():
    data = request.form
    source_text = data['source_text']
    target_language = data['target_language']

    # Translate text using your Hugging Face model
    translation = translator(source_text, target_language=target_language)

    return render_template('index.html', source_text=source_text, target_language=target_language, translation=translation[0]['translation_text'])