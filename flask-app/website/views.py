from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Translation, Feedback
from .model_handler import translate_text
from . import db
import json

views = Blueprint('views', __name__)

#define views
@views.route('/', methods=['GET', 'POST']) #main page of the website
# @login_required
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

    return render_template("newbase.html")


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


# ... (previous code)

# Define a route for handling translation
@views.route('/translate', methods=['GET','POST'])
def translate():
    if request.method == 'POST':
        input_text = request.form['input_text']
        translated_text = translate_text(input_text)

        return render_template('view_translation.html', input_text=input_text, translated_text=translated_text)

