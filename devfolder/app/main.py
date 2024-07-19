
# app/main.py
# Purpose: Define main routes and functionality for the AI Software Factory application
# Description: This file contains the main blueprint and route definitions

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

# Add more routes and views as needed
