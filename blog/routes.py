from Tools.scripts.make_ctype import method
from flask import render_template, redirect, url_for, flash, request, abort
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    # posts = Post.query.filter_by(user_id=current_user.id)
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/post/<int:post_id>')
def details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('details.html', post=post)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        email = form.email.data
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        flash('Successfully created new user.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember)
            flash('you are now logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email or password incorrect', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log out', 'success')
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.username.data is not None:
            current_user.username = form.username.data
        else:
            current_user.username = current_user.username

        if form.password.data is not None:
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        else:
            current_user.password = current_user.password

        db.session.commit()
        flash('Profile updated', 'info')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('profile.html', form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('create post successfully', 'info')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form)


@app.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Delete post successfully.', 'info')
        return redirect(url_for('home'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully.', 'info')
        return redirect(url_for('details', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update.html', form=form)
