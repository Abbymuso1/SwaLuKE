from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models import User_Translation, Feedback, Subscribe, User, User_Added_Translation, Translation
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import csv
from io import StringIO
from . import db

views = Blueprint('views', __name__)

#define the model
model_name = "AbbyMuso1/model_trans_lu_sw_3"  # Replace with your model name
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

#define the views
@views.route('/') #main page of the website
def home():  
    return render_template("base.html", user=current_user)

@views.route('/subscribeform', methods=['GET','POST'])
def subscribeform():
    if request.method == 'POST':
        other_email = request.form.get('other_email')
        subscribe = Subscribe(other_email=other_email)
        db.session.add(subscribe)
        db.session.commit()

        if subscribe:
            return redirect(url_for('views.home'))

@views.route('/contactform', methods=['GET', 'POST'])
def contactform():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        new_feedback = Feedback(name=name, email=email, subject=subject, message=message)
        db.session.add(new_feedback)
        db.session.commit()

        if new_feedback:
            return redirect(url_for('views.home'))

@views.route('/dashboard', methods=['GET', 'POST']) #user dashboard
@login_required
def dashboard():
    utranslations = User_Added_Translation.query.filter_by(user_id=current_user.id).all()
    all_add_translations = User_Added_Translation.query.all()
    translations = User_Translation.query.all()
    user_translations = User_Translation.query.filter_by(user_id=current_user.id).all()
    users = User.query.all()
    return render_template("userdashboard.html", user=current_user, user_translations=user_translations, utranslations=utranslations, all_add_translations=all_add_translations, translations=translations, users=users)

@views.route('/addtranslation', methods=['GET', 'POST']) #Add translation page
@login_required
def addtranslation():
    if request.method == 'POST':
        original_text = request.form.get('original_text')
        translated_text = request.form.get('translated_text')
        new_translation = User_Added_Translation(original_text=original_text, translated_text=translated_text, user_id=current_user.id)
        db.session.add(new_translation)
        db.session.commit()

        if new_translation:
            return redirect(url_for('views.addtranslation'))

    return render_template("add_translation.html", user=current_user)

@views.route('/viewaddtranslation', methods=['GET', 'POST']) #View Added translation page
@login_required
def viewaddtranslation():
    users = User.query.all()
    translations = User_Added_Translation.query.all()
    return render_template("view_add_translation.html", user=current_user, users=users, translations=translations)

@views.route('/edit_add_trans/<int:trans_id>', methods=['GET', 'POST']) #Edit Added translation page
@login_required
def edit_add_trans(trans_id):
    translation_to_edit = User_Added_Translation.query.get(trans_id)

    if not translation_to_edit:
        # Handle the case where the translation with the given ID is not found
        return redirect(url_for('views.viewaddtranslation'))
    
        
  
    if request.method == 'POST':
        # Update the translation object with form data
        translation_to_edit.original_text = request.form.get('original_text')
        translation_to_edit.translated_text = request.form.get('translated_text')
        # Update other fields as needed

        # Save the changes to the database
        db.session.commit()

        # Redirect to the page where you display the translations
        return redirect(url_for('views.viewaddtranslation'))

    return render_template('edit_user_add.html', trans=translation_to_edit, user=current_user)


    user_to_edit = User.query.get(record_id)

    if not user_to_edit:
        return redirect(url_for('views.userprofile'))
    
    if request.method == 'POST':
        user_to_edit.firstname = request.form.get('firstname')
        user_to_edit.email = request.form.get('email')
        
        db.session.commit()
        return redirect(url_for('views.userprofile'))
    
    return render_template('user_profile.html', user=user_to_edit)

@views.route('/del_add_trans/<int:record_id>', methods=['GET', 'POST']) #Delete Added Translation page
@login_required
def del_add_trans(record_id):
    record_to_delete = User_Added_Translation.query.get(record_id)
    if record_to_delete:
        db.session.delete(record_to_delete)
        db.session.commit()
    return redirect(url_for('views.viewaddtranslation'))
   
@views.route('/viewhistory', methods=['GET', 'POST']) #View history of translation requests
@login_required
def viewhistory():
    users = User.query.all()
    translations = User_Translation.query.all()
    return render_template("view_history.html", user=current_user, users=users, translations=translations)

@views.route('/del_history/<int:record_id>', methods=['GET', 'POST']) #Delete history of translation requests
@login_required
def del_history(record_id):
    record_to_delete = User_Translation.query.get(record_id)
    if record_to_delete:
        db.session.delete(record_to_delete)
        db.session.commit()
    return redirect(url_for('views.viewhistory'))

@views.route('/viewfeedback') # View feedback from users (Admin)
@login_required
def viewfeedback():
    feedback = Feedback.query.all()
    return render_template('viewfeedback.html', user=current_user, feedback=feedback)

@views.route('/viewusers')  # View users(Admin)
@login_required
def viewusers():
    users = User.query.all()
    return render_template('view_users.html', user=current_user, users=users)

@views.route('/del_user/<int:record_id>', methods=['GET', 'POST'])  # Delete users (Admin)
@login_required
def del_user(record_id):
    record_to_delete = User.query.get(record_id)
    if record_to_delete:
        db.session.delete(record_to_delete)
        db.session.commit()
    return redirect(url_for('views.viewusers'))

@views.route('/adduser', methods=['GET', 'POST']) # Add users (Admin)
@login_required
def adduser():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        new_user= User(email=email, firstname=firstname, password=generate_password_hash(password1))
        db.session.add(new_user)
        db.session.commit()
        if new_user:
            return redirect(url_for('views.viewusers'))

    return render_template("add_user.html", user=current_user)

@views.route('/viewsubscribe') # View Subscribe requests from users (Admin)
@login_required
def viewsubscribe():
    subscribe = Subscribe.query.all()
    return render_template('view_subcribe_req.html', user=current_user, subscribe=subscribe)

@views.route('/userprofile', methods=['GET', 'POST']) #User Profile
@login_required
def userprofile():
    return render_template("user_profile.html", user=current_user)

@views.route('/update_user/<int:record_id>', methods=['GET', 'POST']) #Update user profile
@login_required
def updateuser(record_id):
    user_to_edit = User.query.get(record_id)

    if not user_to_edit:
        return redirect(url_for('views.userprofile'))
    
    if request.method == 'POST':
        user_to_edit.firstname = request.form.get('firstname')
        user_to_edit.email = request.form.get('email')
        
        db.session.commit()
        return redirect(url_for('views.userprofile'))
    
    return render_template('user_profile.html', user=user_to_edit)

@views.route('/downloadcsv')
def downloadcsv():
    translations = User_Added_Translation.query.all()

    # Create a CSV string using StringIO
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)

    # Write header
    csv_writer.writerow(['Original Text', 'Translated Text'])

    # Write data rows
    for trans in translations:
        csv_writer.writerow([trans.original_text, trans.translated_text])

    # Create a response with the CSV data
    response = Response(csv_data.getvalue(), content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=added_translations.csv'

    return response

@views.route('/translationpage', methods=['GET', 'POST']) #main page of the website
def translation():
    if request.method == 'POST':
        original_text = request.form.get('original_text')
        inputs = tokenizer.encode("translate Luhya to Swahili: " + original_text, return_tensors="pt")
        translation = model.generate(inputs, max_length=90, num_return_sequences=1)
        translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
        
        if translated_text: 
            if current_user.is_authenticated:
                new_translation = User_Translation(original_text=original_text, translated_text=translated_text,user_id=current_user.id)
                db.session.add(new_translation)
                db.session.commit()
                return render_template('base.html', user=current_user, original_text=original_text, translated_text=translated_text)
            else:
                new_translation = Translation(original_text=original_text, translated_text=translated_text)
                db.session.add(new_translation)
                db.session.commit()
                return render_template('base.html', user=current_user, original_text=original_text, translated_text=translated_text)

    return render_template("base.html", user=current_user)

