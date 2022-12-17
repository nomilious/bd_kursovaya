from flask import *

from access import group_required
from db_work import *
from sql_provider import *

bp_prot = Blueprint('bp_prot', __name__, template_folder = 'templates', static_folder = "../static")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), "sql"))

content = {
    "page_title": "Работа с протоколам",
    "title": "Ваши доступные действия",
    "subtitle": "Работа с протоколами",
    "menu": {
        "Посмотреть": 'bp_prot.prot_show',
        "Создать": 'bp_prot.prot_create',
        "Закрыть протоеол": 'bp_prot.prot_close',
    },
    'allowed': {
        "Возврат в главное меню": 'main_menu'
    }
}
@bp_prot.route('/')
@group_required
def start_prot():
    return render_template('make_index.html', content = content)


@bp_prot.route('/show')
@group_required
def prot_show():
    sql = provider.get("select_proto.sql")
    o, c = select_showp(current_app.config ['db_config'], sql)
    return render_template("prot_show.html", opened = o, closed = c)


@bp_prot.route('/create', methods = ["GET", "POST"])
@group_required
def prot_create():
    if request.method == 'GET':
        sql = provider.get("select_equipment.sql")
        content = select_createp(current_app.config ['db_config'], sql)
        sql = provider.get("select_staff.sql")
        content_staff = select_createp(current_app.config ['db_config'], sql)
        return render_template("prot_create.html", content = content, content_staff = content_staff)
    else:
        title = request.form.get("equipment").strip()
        name = request.form.get("report").strip()
        if name and title:
            call_proc(current_app.config ['db_config'], 'create_protocol', title, name)
            return render_template("success.html")
        return render_template("fail.html")


@bp_prot.route('/close', methods = ["GET", "POST"])
@group_required
def prot_close():
    if request.method == 'GET':
        sql = provider.get("select_proto.sql")
        o, _ = select_showp(current_app.config['db_config'], sql)
        return render_template("prot_close.html", opened = o)
    else:
        id = request.form.get("id")
        if id:
            sql = provider.get("select_tests.sql", id = int(id))
            c = select(current_app.config['db_config'], sql)[1]
            cnt, cnt_null = c[0]
            if cnt_null > 0 or cnt == 0:
                return render_template("fail.html", text=f"Нельзя закрыть протокол, пока не будут проведены все "
                                                         f"тесты.", additional=f"Осталось провести {cnt_null} тесты")
            else:
                call_proc(current_app.config['db_config'], 'set_status', id)
                return render_template("success.html")
