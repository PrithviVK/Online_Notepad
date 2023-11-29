from flask import Blueprint,render_template, request, flash, json, jsonify
#Blueprint has a bunch of roots/URL defined inside for the app to work and access the root
from flask_login import login_required, current_user#current user is used to detect if a user is logged in or not
from .models import Note
from . import db

views=Blueprint("views",__name__)#defining the name of the blueprint

# @views.route is a decorator
@views.route('/',methods=['GET','POST']) #views is Blueprint and route is the homepage's route
@login_required# can access home only when user is logged in 
def home():
    if request.method == 'POST':
        note=request.form.get('note')

        if len(note)<1:
            flash("Note is too short!",category='error')
        else:
            new_note=Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Noted added successfully!',category='success')
    
    return render_template("home.html",user=current_user)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    data=json.loads(request.data) #take some data from a POST request and request.data is the string that we passed in index.js i.e., noteId and put in a dictionary object
    note_Id=data['noteId']
    note=Note.query.get(note_Id)#get the note Id and check if the note exists or not
    
    if note:#if we found a note exists
        if note.user_id == current_user.id:# security check if it is the correct user or not to delete a note 
            db.session.delete(note)
            db.session.commit()

    return jsonify({})    # just returning an empty dictionary in the form of a json object      





