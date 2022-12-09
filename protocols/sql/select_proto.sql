SELECT t.date_t, t.status, s.FIO, e.title
FROM test_protocol t
	join staff s on t.id_staff = s.id_s
    join equipment e on t.id_eq = e.id_l
order by t.date_t desc;