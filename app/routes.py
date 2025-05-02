# --- FILE: app/routes.py ---
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import users, credentials
import os, uuid
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

main_bp = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'
KEY = get_random_bytes(16)

def encrypt_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(filepath + ".enc", 'wb') as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
    os.remove(filepath)

@main_bp.route('/')
def home():
    return render_template('login.html')

@main_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    for uid, user in users.items():
        if user.username == username and credentials[username] == password:
            login_user(user)
            return redirect(url_for('main.dashboard'))
    flash('Invalid credentials')
    return redirect(url_for('main.home'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'media' not in request.files:
        flash('No file part')
        return redirect(url_for('main.dashboard'))
    file = request.files['media']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.dashboard'))
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
    file.save(filepath)
    encrypt_file(filepath)
    flash('File uploaded and encrypted!')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
