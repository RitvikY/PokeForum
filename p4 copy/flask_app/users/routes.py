from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
import os
from flask import current_app

from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """



@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        # Redirect to home if user is already logged in
        return redirect(url_for('pokemon.search'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Here we hash the password and create a new User instance
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user.save()  # This saves the new User object to the database

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pokemon.search'))  # Redirect authenticated users to the movies index page.

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('pokemon.search'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()  # This will log out the user
    flash('You have been logged out.', 'info')  # Optional: Flash a message to the user
    return redirect(url_for('pokemon.search'))  # Redirect to the home page or login page



from ..models import Review
# In your users/routes.py

@users.route('/user/<username>')
def user_detail(username):
    user = User.objects.get_or_404(username=username)  # Fetch the user by username

    # Fetch reviews where the author field matches the user
    user_reviews = Review.objects(author=user)

    return render_template('user_detail.html', user=user, user_reviews=user_reviews)


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_picture_form = UpdateProfilePicForm()

    if update_username_form.validate_on_submit() and 'submit_username' in request.form:
        # Update username logic
        current_user.username = update_username_form.username.data
        current_user.save()  # Assume save() properly commits the changes
        flash('Your username has been updated!', 'success')
        return redirect(url_for('users.account'))

    if update_profile_picture_form.validate_on_submit() and 'submit_picture' in request.form:
        # Update profile picture logic
        if update_profile_picture_form.picture.data:
            img = update_profile_picture_form.picture.data
            filename = secure_filename(img.filename)
            content_type = f'image/{filename.rsplit(".", 1)[1].lower()}'

            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(img.stream, content_type=content_type)

            current_user.save()
            flash('Your profile picture has been updated!', 'success')
        else:
            flash('No profile picture uploaded.', 'warning')

        return redirect(url_for('users.account'))

    profile_pic = None
    if request.method == "GET":
        if current_user.profile_pic.get():
            profile_pic = base64.b64encode(current_user.profile_pic.read()).decode('utf-8')

    return render_template('account.html', title='Account',
                           update_username_form=update_username_form,
                           update_profile_picture_form=update_profile_picture_form,
                           profile_pic=profile_pic,
                           user_reviews_url=url_for('users.user_detail', username=current_user.username))