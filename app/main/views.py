from flask import render_template,request,redirect,url_for,abort,request
from ..models import User,Pitch,Comment,Upvote,Downvote
from . import main
from flask_login import login_required,current_user
from .forms import UpdateProfile,PitchForm,CommentForm
from .. import db,photos


# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    pitch = Pitch.query.all()
    education = Pitch.query.filter_by(category = 'education').all()
    music = Pitch.query.filter_by(category = 'music').all()
    religion = Pitch.query.filter_by(category = 'religion').all()

    title = "Welcome to the page"
    
    return render_template('index.html',title = title ,pitch = pitch, education = education, music = music, religion = religion)

@main.route('/new_pitch', methods = ['POST','GET'])

@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title=form.title.data
        pitch=form.post.data
        category=form.category.data
        user_id=current_user
        new_pitch_object=Pitch(pitch=pitch,user_id=current_user._get_current_object().id,category=category,title=title)
        new_pitch_object.save_pitch()

        return redirect(url_for('main.index'))

    return render_template('pitch.html',form=form)

@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])

@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments  = Comment.query.filter_by(pitch_id = pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id, pitch_id = pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', pitch_id = pitch_id))
    return render_template('comment.html', form = form, pitch= pitch, all_comments = all_comments)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    pitch = Pitch.query.filter_by(user_id = user_id).all()

    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user,pitch = pitch)

@main.route('/user/<uname>/update_profile',methods = ['GET','POST'])

@login_required
def update_profile(uname):
    form = UpdateProfile()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/profile',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/upvote/<int:id>',methods = ['POST','GET'])

@login_required
def like(id):
    pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_upvote = Upvote(user = current_user, pitch_id=id)
    new_upvote.save_upvote()
    return redirect(url_for('main.index',id=id))

@main.route('/downvote/<int:id>',methods = ['POST','GET'])

@login_required
def dislike(id):
    pitches = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in pitches:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, pitch_id=id)
    new_downvote.save_downvote()
    return redirect(url_for('main.index',id=id))









