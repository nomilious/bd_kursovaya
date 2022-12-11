# import numpy as np

from access import *
from db_work import *
from sql_provider import *

bp_equip = Blueprint('bp_equip', __name__, template_folder = 'templates', static_folder = "../static")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), "sql"))

content = {
    "page_title": "Работа с оборудованием",
    "title": "Ваши доступные действия",
    "subtitle": "Работа с оборудованием",
    'menu': {
        "Показать открытые отчеты": 'bp_equip.show_tests',
        "Запланировать тесты": 'bp_equip.plan_test',
        "Создать тесты": 'bp_equip.create_test'
    },
    'allowed': {
        "Возврат в главное меню": 'main_menu'
    }
}


@bp_equip.route('/')
@login_required
@group_required
def start_equip():
    return render_template('make_index.html', content = content)


@bp_equip.route("/show-opened")
@login_required
@group_required
def show_tests():
    sql = provider.get("select_opened_proto.sql")
    o, _ = select_showp(current_app.config ['db_config'], sql)
    return render_template("show_test.html", opened = o)


@bp_equip.route("/plan", methods = ['GET', 'POST'])
@login_required
@group_required
def plan_test():
    content = "Select * from equipment_type"
    content = select(current_app.config ['db_config'], content) [1]
    sql = provider.get("select_opened_proto.sql")
    o, _ = select_showp(current_app.config ['db_config'], sql)
    res = np.array(o)
    if request.method == 'POST':
        input = request.form.get("id")
        title = dict(content) [int(input)]
        add_to_basket(int(input), title)
    else:
        clear_basket('bp_equip.plan_test')
    return render_template("plan_test.html", needed = np.unique(res [:, -3]), types = content)


@bp_equip.route("/clear_basket")
@group_required
def clear_basket(redirect_to: str = ''):
    if 'basket' in session:
        del session ['basket']
    if redirect_to != '':
        return redirect(url_for(redirect_to))
    return redirect(url_for(request.args ['redirect_to']))


@bp_equip.route("/save_basket")
@group_required
def save_basket(proc: str = ""):
    if 'basket' not in session:
        return render_template('fail.html')
    if proc == "":
        proc = request.args ['proc']
    for num in session ['basket']:
        call_proc(current_app.config ['db_config'], proc, int(num))
    del session ['basket']
    return render_template("success.html")


def add_to_basket(id, title: str):
    curr_basket = session.get('basket', {})
    if str(id) not in curr_basket:
        curr_basket [str(id)] ['amount'] += curr_basket [prod_id] ['amount'] + 1
    else:
        curr_basket [str(id)] = {
            'id': str(id),
            'title': title,
            'amount': 1,
            'status': []
        }
    session ['basket'] = curr_basket
    session.permanent = True
    return True


def save_tests(pattern, protocol_id, id_tt):
    for status in pattern:
        call_proc(current_app.config ['db_config'], 'create_test', int(status), protocol_id, id_tt)
    return True


@bp_equip.route("/create", methods = ['GET', 'POST'])
@login_required
@group_required
def create_test():
    ttest_day = ""
    if request.method == 'GET':
        if 'basket' in session:
            del session ['basket']
    else:
        if "title" not in request.form:
            for id in request.form:
                save_tests(request.form.get(id), *list(map(int, id.split())))
            return render_template("success.html")
        protocol_id = request.form.get("protocol_id")
        id_tt = request.form.get("id_tt")
        title = request.form.get("title")
        id = f"{protocol_id} {id_tt}"
        add_to_basket(id, title)
        _, ttest_day = select_showp(current_app.config ['db_config'], provider.get("select_ttest_day.sql"))
    _, o = select_showp(current_app.config ['db_config'], provider.get("select_ttest.sql"))
    return render_template("create_test.html", content = o, day_test = ttest_day)