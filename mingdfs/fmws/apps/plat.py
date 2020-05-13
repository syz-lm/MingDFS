from flask import request, session, redirect, url_for, render_template, Blueprint, abort

PLAT_BP = Blueprint('plat_bp', __name__)

@PLAT_BP.route("/login", methods=["GET", "POST"])
def login():
    pass


@PLAT_BP.route("/register", methods=["GET", "POST"])
def register():
    pass


@PLAT_BP.route("/logout", methods=["GET", "POST"])
def logout():
    pass


@PLAT_BP.route('/forget_password', methods=['POST', 'GET'])
def forget_password():
    pass


@PLAT_BP.route('/send_check_code', methods=['POST'])
def send_check_code():
    pass


@PLAT_BP.route('/top_up', methods=['GET', 'POST'])
def top_up():
    pass