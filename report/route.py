from flask import *
from access import *
from db_work import *
from sql_provider import *
import os
from db_context_manager import *

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

bp_report = Blueprint('bp_report', __name__, template_folder='templates', static_folder="../static")

report_list = [
    {'rep_name':'Отчет о работоспособность сотрудников', 'rep_id':'1'},
    {'rep_name':'Отчет по прохождения тестов', 'rep_id':'2'}
]
report_url = {
    '1': {'create_rep':'bp_report.create_rep', 'view_rep':'bp_report.view_rep'},
    '2': {'create_rep':'bp_report.create_rep', 'view_rep':'bp_report.view_rep'}
}
schemas = {
    '1': ['id_сотрудника', 'ФИО', 'Выполнил', 'Команда', 'Численность команды', 'Команда выполнила'],
    "2": ["id_оборудования", "Название", "№ Пртотокола", "Статус протокола", "Кол тестов", "Успешные тесты",
          "ФИО сотрудника проводивший тестирование", "id_сотрудника"]
}


@bp_report.route('/', methods=['GET', 'POST'])
@login_required
@group_required
def start_report():
    if request.method == 'GET':
        return render_template('index_report.html', report_list= report_list)
    else:
        rep_id = request.form.get('rep_id')
        print('rep_id = ', rep_id)
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        print('url_rep = ', url_rep)
        return redirect(url_for(url_rep, rep_id=rep_id))


@bp_report.route('/create_rep', methods=['GET', 'POST'])
@group_required
def create_rep():
    rep_id = request.args.get('rep_id')
    if request.method == 'GET':
        print("GET_create")
        # get rep_name from report_list by rep_id
        rep_name = report_list[int(rep_id)-1]['rep_name']
        return render_template('report_input.html', title= rep_name)
    else:
        print(current_app.config['db_config'])
        print("POST_create")
        rep_year = request.form.get('year')
        rep_month = request.form.get('month')
        print("Loading...")
        if rep_year and rep_month:
            if rep_id == '1' or rep_id == 1:
                res = call_proc(current_app.config['db_config'], 'staff_work_statistic', rep_year, rep_month)
            else:
                res = call_proc(current_app.config['db_config'], 'equipment_testing_statistic', rep_year, rep_month)
            print('res=', res)
            return render_template('success.html')
        else:
            return "Repeat input"


@bp_report.route('/view_rep', methods=['GET', 'POST'])
@group_required
def view_rep():
    rep_id = request.args.get('rep_id')
    rep_name = report_list[int(rep_id) - 1]['rep_name']
    if request.method == 'GET':
        return render_template('report_input.html', title= f"Просмотр отчета \"{rep_name}\"")
    else:
        rep_month = request.form.get('month')
        rep_year = request.form.get('year')
        if rep_year and rep_month:
            _sql = provider.get(f'rep{rep_id}.sql', in_year=rep_year, in_month=rep_month)
            schema, product_result = select(current_app.config['db_config'], _sql)
            if product_result:
                schema = ["id_Оборудования", "Название", "№ Пртотокола", "Статус протокола", "Кол тестов",
                          "Успешные тесты", "ФИО сотрудника проводивший тестирование", "id_сотрудника"]
                return render_template('result.html', schema=schemas[rep_id], result=product_result, title= f"Просмотр "
                                                                                                     f"отчета \"{rep_name}\"")
            else:
                return render_template("fail.html")
        else:
            return "Repeat input"
