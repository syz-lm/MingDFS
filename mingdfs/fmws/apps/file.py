from flask import Blueprint, request

FILE_BP = Blueprint('file_bp', __name__)


@FILE_BP.route('/upload', methods=['GET'])
def upload():
    pass

@FILE_BP.route('/delete', methods=['GET'])
def delete():
    pass

@FILE_BP.route('/edit', methods=['GET'])
def edit():
    pass

@FILE_BP.route('/edit_file_content', methods=['GET'])
def edit_file_content():
    pass