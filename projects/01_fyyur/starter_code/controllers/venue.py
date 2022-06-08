from flask import Blueprint, render_template, abort

venuePage = Blueprint('venuePage', __name__, template_folder: 'templates')
