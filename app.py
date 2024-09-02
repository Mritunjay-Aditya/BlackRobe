from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Disable secure session cookies for local testing
app.config['SESSION_COOKIE_SECURE'] = False  # Change to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
mongo = PyMongo(app)

# Create a new MongoClient instance
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database('judiciary-application')

# Ping the MongoDB deployment
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Email Configuration for Forgot Password
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/')
def home():
    print("Home route accessed. Session:", session)
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("Signup route accessed. Session:", session)
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        user = {
            'full_name': full_name,
            'email': email,
            'password': hashed_password
        }
        
        try:
            result = db.users.insert_one(user)
            if result.acknowledged:
                flash('Signup successful! Please log in.', 'success')
            else:
                flash('Signup failed! Please try again.', 'danger')
        except Exception as e:
            flash(f'Error inserting user: {str(e)}', 'danger')
            print(f'Error inserting user: {str(e)}')
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route accessed. Session:", session)
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Attempting login with email: {email}")

        try:
            user = db.users.find_one({'email': email})
            if user:
                print(f"User found: {user['_id']}, {user['full_name']}")
            else:
                print("User not found with this email.")
        except Exception as e:
            flash(f'Error finding user: {str(e)}', 'danger')
            print(f'Error finding user: {str(e)}')
            return redirect(url_for('login'))
        
        if user and check_password_hash(user['password'], password):
            print("Password is correct.")
            session.clear()  # Clear any existing session data
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['full_name']  # Store the user's name in the session
            print(f"Session after login: {session}")
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
            print("Login failed: Invalid email or password.")
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    print("Dashboard route accessed. Session:", session)
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        print("Access to dashboard denied. No user_id in session.")
        return redirect(url_for('login'))
    
    user_name = session.get('user_name')
    print(f"Accessing dashboard. User: {user_name}")
    return render_template('dashboard.html', user_name=user_name)

@app.route('/logout')
def logout():
    print("Logout route accessed. Clearing session:", session)
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = db.users.find_one({'email': email})
        
        if user:
            token = s.dumps(email, salt='email-confirm')
            link = url_for('reset_password', token=token, _external=True)
            
            msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f'Your link to reset the password is {link}. The link is valid for 30 minutes.'
            mail.send(msg)
            
            flash('Password reset link has been sent to your email.', 'info')
        else:
            flash('No account found with this email!', 'danger')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=1800)  # 30 minutes expiration
    except SignatureExpired:
        flash('The token is expired!', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('reset_password', token=token))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            db.users.update_one({'email': email}, {'$set': {'password': hashed_password}})
            flash('Your password has been updated!', 'success')
        except Exception as e:
            flash(f'Error updating password: {str(e)}', 'danger')
            print(f'Error updating password: {str(e)}')
        
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.debug = True  # Enable debugging
    app.run(host="0.0.0.0", port=33)
