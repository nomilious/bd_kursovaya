import time

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
    select_v = {}
    sql = provider.get("select_totest.sql")
    content = select(current_app.config['db_config'], sql)[1]

    if request.method == 'POST':
        protocol_id = request.form.get("protocol_id")
        title = request.form.get("title")
        eq_t = request.form.get("eq_t")
        add_to_basket(protocol_id, title, eq_t)
        select_v = transform_to_dict(
            list(select(current_app.config['db_config'], provider.get("select_test_types.sql"))[1])
            )
    else:
        clear_basket('bp_equip.plan_test')
    return render_template("plan_test.html", min_date = time.strftime('%Y-%m-%d'), content = content, select = select_v)


@bp_equip.route("/clear_basket")
def clear_basket(redirect_to: str = ''):
    if 'basket' in session:
        del session ['basket']
    if redirect_to != '':
        return redirect(url_for(redirect_to))
    return redirect(url_for(request.args ['redirect_to']))


@bp_equip.route("/save", methods = ['POST'])
def save_basket():
    if 'basket' not in session:
        return render_template('fail.html')
    ids = request.form.getlist('protocol_id')
    types = request.form.getlist('test_type')
    dates = request.form.getlist('test_date')
    eqtypes = request.form.getlist('eq_t')
    for i in range(len(ids)):
        call_proc(current_app.config['db_config'], 'plan_test', int(eqtypes[i]), int(ids[i]), types[i], dates[i])
    del session['basket']
    return render_template("success.html")


@bp_equip.route("/save_results", methods = ['POST'])
def save_results():
    if 'basket' not in session:
        return render_template('fail.html')
    ids = request.form.getlist('id')
    statuses = request.form.getlist('status')
    for i in range(len(ids)):
        res = call_proc(current_app.config['db_config'], 'create_test', int(statuses[i]), int(ids[i]))
        print(res)
    return render_template("success.html")


def add_to_basket(id: str, title: str, eq_t: int):
    curr_basket = session.get('basket', {})
    if id not in curr_basket:
        curr_basket[id] = {
            'id': id,
            't_id': eq_t,
            'title': title,
            'count': 1
        }
    else:
        curr_basket[id]['count'] += 1
    session['basket'] = curr_basket
    session.permanent = True
    return True


def transform_to_dict(a):
    res = {}
    for line in a:
        if str(line [0]) not in res:
            res [str(line [0])] = [line [1]]
        else:
            res[str(line[0])].append(line[1])
    return res


def save_tests(pattern, protocol_id, id_tt):
    for status in pattern:
        call_proc(current_app.config['db_config'], 'create_test', int(status), protocol_id, id_tt)
    return True


def transform_grouped(o):
    res = {}
    for line in o:
        if line[-1] not in res:
            res[line[-1]] = [line]
        else:
            res[line[-1]].append(line)
    return res


@bp_equip.route("/create", methods = ['GET', 'POST'])
@login_required
def create_test():
    ttest_day = ""
    if request.method == 'GET':
        if 'basket' in session:
            del session['basket']
    else:
        protocol_id = request.form.get("protocol_id")
        id = request.form.get("id")
        title = request.form.get("title")
        add_to_basket(id, title, protocol_id)
        # _, ttest_day = select_showp(current_app.config ['db_config'], provider.get("select_ttest_day.sql"))
    o = select(current_app.config['db_config'], provider.get("select_ttest.sql"))[1]
    return render_template("create_test.html", content = transform_grouped(o), day_test = ttest_day)