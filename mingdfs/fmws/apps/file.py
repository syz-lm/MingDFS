from flask import request, session, redirect, url_for, render_template, Blueprint, abort

FILE_BP = Blueprint('file_bp', __name__)


@FILE_BP.route('/upload', methods=['GET', 'POST'])
def upload():
    pass


@FILE_BP.route('/download', methods=['GET', 'POST'])
def download():
    pass


@FILE_BP.route('/edit', methods=['GET', 'POST'])
def edit():
    pass


@FILE_BP.route('/delete', methods=['GET', 'POST'])
def delete():
    pass