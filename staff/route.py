from flask import *
from access import *


bp_staff = Blueprint('bp_staff', __name__, template_folder='templates', static_folder="../static")


@bp_staff.route('/')
@login_required
@group_required
def start_staff():
    return render_template('index_staff.html')


@bp_staff.route("/show-all")
@login_required
@group_required
def show_all():
    return render_template("show_allstaff.html")


@bp_staff.route("/show_custom")
@login_required
@group_required
def show_custom():
    return render_template("show_customstaff.html")
