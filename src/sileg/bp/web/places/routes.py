from flask import render_template, flash, redirect,request, Markup, url_for

from . import bp

@bp.route('/crear')
def create():
    """
    Pagina principal de usuarios
    """
    return render_template('places.html')

@bp.route('/buscar')
def search():
    """
    Pagina principal de usuarios
    """
    return render_template('places.html')