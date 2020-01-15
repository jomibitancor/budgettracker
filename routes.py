from flask import render_template, url_for, flash, redirect, request
from btracker import app, db, bcrypt, mail # IMPORT: Since routes.py uses @app.route #IMPORT: db, bcrypt from the package
from btracker.models import User, Budget, Entries
from btracker.forms import (RegistrationForm, LoginForm, NewEntryForm, NewBudgetForm,
    RequestResetForm, ResetPasswordForm) # IMPORT: Get the forms from the forms.py file
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
def intro():
    return render_template('intro.html')
    
@app.route("/home")
@login_required
def home():
    if Budget.query.filter_by(user_id=current_user.id).first() != None:
        current_budget = Budget.query.filter_by(user_id=current_user.id).first().budget
        page = request.args.get('page', type=int)
        
        user_entries = Entries.query.filter_by(user_id=current_user.id)

        total_spent = 0
        for entry in user_entries:
            total_spent += entry.amount

        order_by = request.args.get('order', type=int)
        if order_by == 2:
            entries_list = user_entries.order_by(Entries.date_posted).paginate(page=page, per_page=10)
        elif order_by == 3:
            entries_list = user_entries.order_by(Entries.amount).paginate(page=page, per_page=10)
        elif order_by == 4:
            entries_list = user_entries.order_by(Entries.amount.desc()).paginate(page=page, per_page=10)
        else:
            entries_list = user_entries.order_by(Entries.date_posted.desc()).paginate(page=page, per_page=10)
             
        return render_template('home.html', current_budget=current_budget, entries_list=entries_list, total_spent=total_spent)
    else:
        return redirect(url_for('new_budget')) 

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # IMPORT: from flask_login import current_user
        return redirect(url_for('home'))
    form = RegistrationForm() # Create an instance of the form and then send it to our application
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success') # IMPORT from flask import flash
        return redirect(url_for('login')) # IMPORT from flask import redirect
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # IMPORT: from flask_login import current_user
        return redirect(url_for('home'))
    form = LoginForm() # Create an instance of the form and then send it to our application
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) # Log them in # IMPORT: from flask_login import login_user
            next_page = request.args.get('next') # IMPORT: from flask import request
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed. Please try again', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user() # IMPORT: from flask_login import logout_user
    return redirect(url_for('home'))

@app.route("/entry", methods=['GET','POST'])
@login_required
def new_entry():
    form = NewEntryForm()
    if form.validate_on_submit():
        entry = Entries(amount=form.amount.data, category=form.category.data, comment=form.comment.data, user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()
        flash('Submitted', 'success')
        return redirect(url_for('home'))
        
    return render_template('new_entry.html', title='Entry', form=form, legend='New Entry')

@app.route("/setabudget", methods=['GET', 'POST'])
@login_required
def new_budget():
    form = NewBudgetForm()
    past_budget = Budget.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        if past_budget != None:
            db.session.delete(past_budget)
            db.session.commit()

        budget = Budget(budget=form.budget.data, user_id=current_user.id)
        db.session.add(budget)
        db.session.commit()
        flash('Budget Added', 'success')
        return redirect(url_for('home'))

    return render_template('new_budget.html', title='Enter A Budget', form=form, past_budget=past_budget)

@app.route("/entry/<int:eid>/update", methods=['GET', 'POST'])
@login_required
def update_entry(eid):
    entry = Entries.query.get_or_404(eid)
    if entry.user_id != current_user.id:
        abort(403)
    form = NewEntryForm()
    if form.validate_on_submit():
        entry.amount = form.amount.data
        entry.category = form.category.data
        entry.comment = form.comment.data
        db.session.commit()
        flash('Entry updated!', 'success')
        return redirect(url_for('home'))
    form.amount.data = entry.amount
    form.category.data = entry.category
    form.comment.data = entry.comment

    return render_template('new_entry.html', title='Update Entry', form=form, legend='Update Entry')

@app.route("/entry/<int:eid>/delete", methods=['GET','POST'])
@login_required
def delete_entry(eid):
    entry = Entries.query.get_or_404(eid)
    if entry.user_id != current_user.id:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash('Your entry has been deleted!', 'success')
    return redirect(url_for('home'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Request Form', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to the email with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form = form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password updated!', 'success')
        return redirect(url_for('login')) 
    return render_template('reset_token.html', title='Reset Password', form = form)