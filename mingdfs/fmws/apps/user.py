from flask import request, session, redirect, url_for, render_template, Blueprint, abort

USER_BP = Blueprint('USER_BP', __name__)


@USER_BP.route('/login', methods=['GET', 'POST'])
def login():
    pass


@USER_BP.route('/register', methods=['GET', 'POST'])
def register():
    pass


@USER_BP.route('/change_password', methods=['GET', 'POST'])
def change_password():
    pass


@USER_BP.route('/logoout', methods=['GET', 'POST'])
def logout():
    pass


@USER_BP.route('/send_email_check_code', methods=['GET', 'POST'])
def send_email_check_code():
    pass