from flask import *
import os
from sql_provider import *
from db_work import *

bp_auth = Blueprint('bp_auth', __name__, template_folder='templates', static_folder="../static")
provider = SQLProvider(os.path.join(os.path.dirname(__file__), "sql"))


@bp_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    template = "login.html"
    if request.method == 'GET':
        return render_template(template)
    else:
        login = request.form.get("login")
        password = request.form.get("password")
        if login:
            user_info = define_user(login, password)
            if user_info:
                user_dict = user_info[0]
                session['user_id']= user_dict['user_id']
                group = user_dict['user_group']
                session['user_group'] = group if group else "external"
                session.permanent = False
                return redirect(url_for('main_menu'))
            else:
                return render_template(f"bad_{template}", message="User not found")
        return render_template(template, message="Try again")


def define_user(login: str, password:str):
    sql_internal = provider.get("login.sql", login=login, password=password)

    user_info = select_dict(current_app.config['db_config'], sql_internal)
    return user_info
