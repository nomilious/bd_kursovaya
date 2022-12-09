from flask import *
from access import login_required, group_required
from db_work import *
from sql_provider import *

bp_prot = Blueprint('bp_prot', __name__, template_folder='templates', static_folder="../static")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), "sql"))


@bp_prot.route('/')
@login_required
@group_required
def start_prot():
    return render_template('menu_prot.html')


@bp_prot.route('/show')
@group_required
def prot_show():
    sql = provider.get("select_proto.sql")
    o, c = select_showp(current_app.config['db_config'], sql)
    return render_template("prot_show.html", opened=o, closed=c)


@bp_prot.route('/create', methods=["GET", "POST"])
@group_required
def prot_create():
    if request.method == 'GET':
        sql = provider.get("select_equipment.sql")
        content = select_createp(current_app.config['db_config'], sql)
        sql = provider.get("select_staff.sql")
        content_staff = select_createp(current_app.config['db_config'], sql)
        return render_template("prot_create.html", content=content, content_staff=content_staff)
    else:
        title = request.form.get("equipment").strip()
        name = request.form.get("staff").strip()
        if name and title:
            call_proc(current_app.config['db_config'],'create_protocol', title, name)
            return render_template("success.html")
        return render_template("fail.html")