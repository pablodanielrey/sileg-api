from flask import render_template, flash, redirect,request, Markup, url_for

from . import bp

@bp.route('/')
def users():
    """
    Pagina principal de usuarios
    """
    return render_template('users.html')
    
