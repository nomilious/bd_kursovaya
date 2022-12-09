import json
from pymysql import connect
from faker import Faker
with open("config/dbconfig.json", "r") as f:
     config: dict = json.load(f)
faker = Faker()
n=0
conn = connect(**config)
for i in range(200):
    cursor = conn.cursor()
    cursor.execute(f"Select id_eq, date_t from  test_protocol where id_p = {i}")
    current_num, current_date = cursor.fetchall()[0]
    cursor2 = conn.cursor()
    cursor2.execute(f"""
    Select t.id_tt
    from (
        SELECT id_t, max(date_tt) as dtt
        FROM ttest_plan 
        where id_t= (
            Select eq_t from equipment 
            where id_l = {current_num}
        )
            and date_tt <= '{current_date}'
        group by id_t
    ) outt join ttest_plan t
    where outt.dtt = date_tt and outt.id_t = t.id_t
    """)
    # print(cursor2.fetchall())
    res = cursor2.fetchall()[0][0]

    for j in range(1, faker.random_int(1, 3)+1):
        zapr = ""
        # zapr += "("
        # zapr += f"{n},"
        # zapr += f"{faker.random_int(0, 1)},"
        # zapr += f"{i},"
        # zapr += f"{res}"
        # zapr += "),"
        zapr += str(current_num) + " " + str(current_date) + " = " + str(res)
        print(zapr)
        n += 1
# >>> tests
# [7, 2, 2, 5, 3]
#
# id_p date_t status id_staff     id_eq - 1
# id status tt_test_id protocol_id  - 2

from faker import Faker

faker = Faker()
print("Insert into test_equip.test_protocol values")
for i in range(len(res)):
    zapr = ""
    zapr+= "("
    zapr+= f"{100+i},"
    zapr+= f"'{faker.date_this_month(True, True)}',"
    zapr+= "NULL,"
    zapr+= f"{faker.random_int(0, 99)},"
    zapr+= f"{res[i][0]}"
    zapr+= "),"
    print(zapr)

print("Insert into test_equip.list_of_testing values")
n = 0
for i in range(200):
    date = faker.random_int(0, 99)
    prot_id = faker.random_int(0, 200)
    for j in range(1, faker.random_int(1, 4)):
        zapr = ""
        zapr+= "("
        zapr+= f"{n},"
        zapr+= f"{faker.random_int(0, 1)},"
        zapr+= f"{prot_id},"
        zapr+= "),"
        print(zapr)
        n+=1
