from flask import (Flask,  g, render_template, 
                    flash, redirect, url_for, abort)
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import models
import forms


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = flask(__name__)
app.secret_key = 'yhfglgfaligufauirgarughdfbdkfbdfbdkfdkfbkdf'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager_user_loader
def load_user(userid):
    try:
        return models.User.get(models,User,id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to database before request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user=current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    b.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("you have been  registered", "sucess")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            passowrd=form.passowrd.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = formsLoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or Password doesnt match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("you have been logged in ", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesnt match", "error")
    return render_template('login.html', form=form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("logout sucessful!")
    return redirect(url_for('index'))

@app.route('/new_post',methods=('GET', 'POST'))
@login_required
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user.g.user._get_current_object(), 
                            content=form.content.data.strip())
        flash("Message Posted thanks", "success")
        return redirect(url_for('index'))
    return render_template('post.html', form=form)



@app.route('/')
def index():
    stream = models.post.select().limit(100)
    return render_template('stream.html', stream=stream)


@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
    template='stream.html'
    if username and username != current_user.username:
       try:
            user = models.User.select().where(mdoels.User.username**username).get()
            stream = user.posts.limit(100)
        except models.DoesNotExist:
            abort(404)
    else:
        stream = current_user.get_stream().limit(100)
        user = current_user
    if username:
        template = 'user_stream.html'
    return render_template(template, stream=stream, user=user)

@app.route('/post/<int: post_id>')
def view_post(post_id):
    posts = models.Post.select().where(models.Post.id ==post.id)
    return render_template('stream.html', stream=posts)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    models.initialize()
    try:
        
    except ValueError:
        pass

    app.run(debug=TRUE, host=host, port=PORT)

