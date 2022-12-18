from flask import render_template, flash, redirect, url_for
from flask_login import login_user, LoginManager, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models.models import Users, Notes
from forms.login import Login
from forms.signup import Signup
from mail.mail import welcome
from forms.notes import Note
from forms.upload import Upload

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return Users().query.get(int(id))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    note_form = Note()
    if form.validate_on_submit():
        user = Users().query.filter_by(user_name=form.user_name.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                id = int(current_user.id)
                user_notes = Notes().query.filter_by(user_id=id).all()
                return redirect(url_for('notes', notes=user_notes, form=note_form))
            else:
                flash('Wrong username or password. Please try again')
        else:
            flash('User name not found! Please try with correct user name')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signup()
    if form.validate_on_submit():
        user = None
        try:
            print('here')
            user = Users().query.filter_by(user_name=form.user_name.data).first()
            print('here1')
            if user is not None:
                flash('Given user name already exists in application. So please login')
            else:
                user = Users().query.filter_by(email=form.email.data).first()
                if user is not None:
                    flash('Given user email already exists in application. So please login')
        except:
            pass
        if user is None:
            user = Users(name=form.name.data, user_name=form.user_name.data, email=form.email.data,
                         password=generate_password_hash(form.confirm_password.data))
            db.session.add(user)
            db.session.commit()
            welcome(form.email.data)
            flash('New user created successfully. Please login via login page.')
        form.name.data = ''
        form.user_name.data = ''
        form.email.data = ''
        form.password.data = ''
        form.confirm_password.data = ''

    return render_template('signup.html', form=form)


@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    form = Note()
    user_notes = Notes().query.filter_by(user_id=int(current_user.id)).all()
    if form.validate_on_submit():
        user_notes = Notes(user_id=int(current_user.id), title=form.title.data, notes=form.note.data)
        form.title.data = ''
        form.note.data = ''
        db.session.add(user_notes)
        db.session.commit()
        user_notes = Notes().query.filter_by(user_id=int(current_user.id)).all()
        return redirect(url_for('notes', notes=user_notes, form=form))

    return render_template('notes.html', notes=user_notes, form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = Note()
    user_notes = Notes().query.filter_by(notes_id=id).first()
    if form.validate_on_submit():
        user_notes.title = form.title.data
        user_notes.notes = form.note.data
        db.session.add(user_notes)
        db.session.commit()
        user_notes_all = Notes().query.filter_by(user_id=current_user.id).all()
        form.title.data = ''
        form.note.data = ''
        return redirect(url_for('notes', notes=user_notes_all, form=form))

    form.title.data = user_notes.title
    form.note.data = user_notes.notes

    return render_template('edit.html', form = form)

@app.route('/delete_notes/<int:id>')
@login_required
def delete_notes(id):
    form = Note()
    user_notes = Notes().query.filter_by(notes_id = id).first()
    if user_notes is not None:
        db.session.delete(user_notes)
        db.session.commit()
        user_notes = Notes().query.filter_by(user_id=current_user.id).all()
        return  redirect(url_for('notes',notes=user_notes,form=form))

    user_notes = Notes().query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html',notes=user_notes,form = form)

@app.route('/admin')
@login_required
def admin():
    form = Note()
    user_notes = Notes().query.filter_by(user_id=current_user.id).all()
    if current_user.user_name == 'admin':
        user = Users().query.all()
        return render_template('admin.html', users=user)
    else:
        flash("You don't have access for admin page!")

    return render_template('notes.html', notes=user_notes, form=form)

@app.route('/delete_users/<int:id>')
@login_required
def delete(id):
    user = Users().query.filter_by(id = id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        user = Users().query.all()
        return redirect(url_for('admin',users=user))

    user = Users().query.all()
    return render_template('admin.html', users=user)

@app.route('/Image', methods=['GET', 'POST'])
@login_required
def file_upload():
    form = Upload()
    if form.validate_on_submit():
        form.file.data = ''
        return redirect(url_for('file_upload', form=form))

    return  render_template('image.html', form=form)

@app.errorhandler(404)
def error(e):
    return render_template('error.html'), 404


@app.before_first_request
def create_table():
    db.create_all()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
