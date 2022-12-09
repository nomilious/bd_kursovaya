SELECT t.date_t, t.status, e.title, e.eq_t, tt.type, e.status_update_date, e.status
FROM test_protocol t
    join equipment e on t.id_eq = e.id_l
    join equipment_type tt on e.eq_t = tt.id_t
where t.status is NULL