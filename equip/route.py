from flask import *
from access import *
from sql_provider import *
from db_work import *
from sql_provider import *
import numpy as np

bp_equip = Blueprint('bp_equip', __name__, template_folder='templates', static_folder="../static")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), "sql"))

@bp_equip.route('/')
@login_required
@group_required
def start_equip():
    return render_template('index_equip.html')


@bp_equip.route("/show-opened")
@login_required
@group_required
def show_tests():
    sql = provider.get("select_opened_proto.sql")
    o, _ = select_showp(current_app.config['db_config'], sql)
    return render_template("show_test.html", opened=o)


@bp_equip.route("/plan", methods=['GET', 'POST'])
@login_required
@group_required
def plan_test():
    content = "Select * from equipment_type"
    content = select(current_app.config['db_config'], content)[1]
    sql = provider.get("select_opened_proto.sql")
    o, _ = select_showp(current_app.config['db_config'], sql)
    res = np.array(o)
    if request.method == 'POST':
        input = request.form.get("id")
        title = dict(content)[int(input)]
        add_to_basket(int(input), title)
    else:
        clear_basket('bp_equip.plan_test')
    return render_template("plan_test.html", needed=np.unique(res[:, -3]), types=content)


@bp_equip.route("/clear_basket")
@group_required
def clear_basket(redirect_to: str = ''):
    if 'basket' in session:
        del session['basket']
    if redirect_to != '':
        return redirect(url_for(redirect_to))
    return redirect(url_for(request.args['redirect_to']))


@bp_equip.route("/save_basket")
@group_required
def save_basket(proc: str = ""):
    if 'basket' not in session:
        return render_template('fail.html')
    if proc == "":
        proc = request.args['proc']
    for num in session['basket']:
        call_proc(current_app.config['db_config'], proc, int(num))
    del session['basket']
    return render_template("success_equip.html")


def add_to_basket(id, title: str):
    curr_basket = session.get('basket', {})
    if str(id) not in curr_basket:
        curr_basket[str(id)] = dict(zip(
            ('id', 'title'), (id, title)
        ))
    session['basket'] = curr_basket
    session.permanent = True
    return True

def save_tests(pattern, protocol_id, id_tt):
    for status in pattern:
        call_proc(current_app.config['db_config'], 'create_test', int(status), protocol_id, id_tt )
    return True

@bp_equip.route("/create", methods=['GET', 'POST'])
@login_required
@group_required
def create_test():
    if request.method == 'GET':
        if 'basket' in session:
            del session['basket']
    else:
        if "title" not in request.form:
            for id in request.form:
                save_tests(request.form.get(id), *list(map(int, id.split())))
            return render_template("success_equip.html")
        protocol_id = request.form.get("protocol_id")
        id_tt = request.form.get("id_tt")
        title = request.form.get("title")
        id = f"{protocol_id} {id_tt}"
        add_to_basket(id, title)
    _, o = select_showp(current_app.config['db_config'], provider.get("select_ttest.sql"))
    return render_template("create_test.html", content=o)


