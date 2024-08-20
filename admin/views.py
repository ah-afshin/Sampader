from flask import Blueprint, render_template


admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates')

@admin_bp.route('/admin')
def admin_dashboard():
    return "<p> nothing right now </p>"