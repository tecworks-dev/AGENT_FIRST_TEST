# Purpose: Admin panel routes
# Description: This file contains routes for administrative functions such as retrieving users,
#              banning users, and deleting groups or channels.

import traceback
from flask import Blueprint, request, jsonify, render_template, current_app, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Group, Channel
from app import db

admin = Blueprint('admin', __name__)

DEBUG = True

@admin.route('/')
@login_required
def admin_panel():
    """
    Renders the admin panel interface.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login', next=request.url))
    if not current_user.is_admin:
        return redirect(url_for('root'))
    return render_template('admin_interface.html')

# ... (rest of the file remains unchanged)