from flask import *
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for("bp_auth.start_auth"))
    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_func = request.endpoint # имя обработчика
    endpoint_app = request.endpoint.split('.')[0] # имя blueprint'a
    if 'user_group' in session:
        user_group = session['user_group']
        print(f"You are {user_group}")
        print(f"Needed  {endpoint_func} or {endpoint_app}")
        print(f"Rights {config[user_group]}")
        if user_group in config and endpoint_app in config[user_group]:
            return True
        elif user_group in config and endpoint_func in config[user_group]:
            return True
        return False
    return False


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return render_template("access_refused.html")
    return wrapper
