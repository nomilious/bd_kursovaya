import json

from faker import Faker
from pymysql import connect

with open("'/Users/eduardbelic/PycharmProjects/kursovaya/config/dbconfig.json", "r") as f:
    config: dict = json.load(f)
faker = Faker()
n = 0
conn = connect(**config)


def get_date(id):
    cursor = conn.cursor()
    cursor.execute(f"Select date_t from  test_protocol where id_p = {id}")
    return cursor.fetchall() [0]


def get_test_type_intervals(protocol_id):
    cursor = conn.cursor()
    cursor.execute(f"""select min(id_tt) as min, max(id_tt) as max
        from type_tests tt
        where id_t = (
            select eq_t 
            from test_protocol tp 
            join equipment e on tp.id_eq = e.id_l
            where id_p = {protocol_id} 
        )"""
                   )
    return cursor.fetchall() [0]


print("Insert into test_equip.list_of_testing values")
for i in range(201):
    prot_id = i
    c = 0
    while c == 0:
        c = faker.random_int(0, 1)
        min, max = get_test_type_intervals(prot_id)
        zapr = ""
        zapr += "("
        zapr += f"NULL,"
        zapr += f"{faker.random_int(0, 1)},"
        mydate = get_date(prot_id) [0]
        zapr += f"{prot_id},"
        zapr += f"{faker.random_int(min, max)}"
        zapr += f"'{faker.date_between_dates(mydate - timedelta(days = 7), mydate + timedelta(days = 21))}'"
        zapr += "),"
        print(zapr)


def get_max_type_id():
    cursor = conn.cursor()
    cursor.execute(f"Select max(id_t) from  equipment_type")
    return cursor.fetchall() [0] [0]


for i in range(1, get_max_type_id() + 1):
    for j in range(1, faker.random_int(4, 15)):
        zapr = ""
        zapr += "( NULL,"
        zapr += f"'Тест {j}',"
        zapr += f"{i}"
        zapr += "),"
        print(zapr)