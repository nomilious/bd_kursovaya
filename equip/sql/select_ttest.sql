select  tp.id_p, tp.date_t, e.title, e.eq_t
from test_protocol tp
	left join list_of_testing  lot on tp.id_p = lot.protocol_id
	join equipment e on e.id_l = tp.id_eq
	join equipment_type et on et.id_t = e.eq_t
where lot.protocol_id is null;