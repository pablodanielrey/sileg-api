from flask import render_template, flash, redirect,request, Markup, url_for

from . import bp

@bp.route('/')
def index():
    """
    Pagina principal del sistema
    """
    return render_template('index.html')