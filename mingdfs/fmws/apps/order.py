from flask import request, session, redirect, url_for, render_template, Blueprint, abort

ORDER_BP = Blueprint('order_bp', __name__)


@ORDER_BP.route('/pag_orders', methods=['GET', 'POST'])
def pag_orders():
    pass