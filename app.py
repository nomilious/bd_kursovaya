from auth.route import *
from equip.route import *
from protocols.route import *
from staff.route import *

app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.secret_key = "You will never guess"

app.register_blueprint(bp_prot, url_prefix = '/prot')
app.register_blueprint(bp_auth, url_prefix = '/auth')
app.register_blueprint(bp_equip, url_prefix = '/equip')
app.register_blueprint(bp_staff, url_prefix = '/staff')

content = {
    "page_title": "Главное меню ИС",
    "title": "ИC тестирование оборудования",
    "subtitle": "",
    "menu": {
        "Протоколы": 'bp_prot.start_prot',
        "Оборудование": 'bp_equip.start_equip',
        "Персонал": 'bp_staff.start_staff',
    },
    'allowed': {
        "Выход": 'exit'
    }
}

with open("config/dbconfig.json", 'r') as f:
    config = json.load(f)

with open("config/aсcess.json", 'r') as f:
    access_config = json.load(f)

app.config ['access_config'] = access_config
app.config ['db_config'] = config


@app.template_global()
def has_access(bp):
    user_group = session['user_group']
    accesses = app.config['access_config'][user_group]
    print(accesses, f"blueprint={bp}")
    if bp in accesses:
        return True
    if bp.split('.') [0] in accesses:
        return True
    return False


@app.route('/', methods = ['GET', 'POST'])
@login_required
def main_menu():
    content ['subtitle'] = f"Вы вошли в систему как {session ['user_group'].upper()}",
    return render_template('make_index.html', content = content)


@app.route('/exit')
def exit():
    if 'user_id' in session:
        session.clear()
    return render_template("exit.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001)
#внешний пользователь - тестировщик. только составление тесты. такое-то оборудование. в такойто день тестируется.
# показать
#TODO создать процедуру которая инсертит в ttest_date_plan. на сайте показать нужный протокол тестирования
#TODO создать процедуру которая инсертит в ttest_date_plan
