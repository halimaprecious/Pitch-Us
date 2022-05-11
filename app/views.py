
from .models import Pitch,User,Comment,Like
from flask import Blueprint, flash, render_template, request,redirect, session,url_for
from flask_login import login_required,current_user
from .forms import UpdateProfile,PitchForm
from . import db,photos

views = Blueprint("views",__name__)

@views.route('/')
@login_required
def home():
   pitches = Pitch.query.all()
  
   return render_template('home.html',user = current_user.username,pitches=pitches)

@views.route('/pitch/',methods=['GET','POST'])
@login_required
def pitch():

   form =PitchForm()
   if form.validate_on_submit():
      category = form.category.data
      text =form.text.data
      if not text:
         flash("Pitch cannot be blank",category = 'error')
      else:
         pitch = Pitch(category=category,text=text,author = current_user.id)
         db.session.add(pitch)
         db.session.commit()
         flash('Pitch Sent!',category = 'success')

         return redirect(url_for('views.home'))

   return render_template('pitch-us.html',user=current_user,form =form)

#user profile
@views.route('/user/<username>')
def profile(username):
   user = User.query.filter_by(username=username).first()
   if not user:
      flash("User does not exist!",category='error')

   return render_template("profile/profile.html", user = user)

#update profile
@views.route('/user/<username>/update',methods =['GET','POST'])
@login_required
def update_profile(username):
   user = User.query.filter_by(username = username).first()
   if not user:
      flash("User does not exist!",category='error')

   form = UpdateProfile()
   if form.validate_on_submit():
      user.bio = form.bio.data
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('.profile',username=user.username))

   return render_template('profile/update.html',form =form)

#profile pic
@views.route('/user/<username>/update/pic',methods=['POST'])
@login_required
def update_pic(username):
   user = User.query.filter_by(username=username).first()
   if 'photo' in request.files:
      filename = photos.save(request.files['photo'])
      path = f'photos/{filename}'
      user.profile_pic_path = path
      db.session.commit()
   return redirect(url_for('views.profile',username=username))

# User's pitch
@views.route('/pitch/<username>')
@login_required
def pitches(username):
   user = User.query.filter_by(username=username).first()

   if not user:
      flash("No user with that username!",category='error')
      return redirect(url_for('views.home'))

   pitch = Pitch.query.filter_by(author=user.id).all()
   return render_template('pitch.html',user=current_user, pitch=pitch,username=username)

# comments route
@views.route('/comment/<pitch_id>',methods=['POST'])
@login_required
def comment(pitch_id):
   text = request.form.get('text')

   if not text:
      flash('comment cannot be empty',category='error')
   else:
      pitch = Pitch.query.filter_by(id=pitch_id)
      if pitch:
         comment = Comment(text = text, author=current_user.id, pitch_id= pitch_id)
         db.session.add(comment)
         db.session.commit()
      else:
         flash('Post does not exist!',category='error')
       
   return redirect(url_for('views.home'))

# likes route
@views.route('/like/<pitch_id>',methods=['GET'])
@login_required
def like(pitch_id):
   pitch = Pitch.query.filter_by(id=pitch_id).first()
   like =Like.query.filter_by(author=current_user.id, pitch_id = pitch_id).first()
   
   if not pitch:
      flash('Post does not exist',category='error')
   elif like:
      db.session.delete(like)
      db.session.commit()
   else:
      like = Like(author=current_user.id, pitch_id=pitch_id)
      db.session.add(like)
      db.session.commit()

   return redirect(url_for('views.home'))






