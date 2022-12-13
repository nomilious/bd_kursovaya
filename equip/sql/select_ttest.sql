select lot.id, lot.protocol_id, tt.name_tt, lot.date_test, e.title
from list_of_testing lot
	join type_tests tt on tt.id_tt = lot.id_test_type
	join test_protocol tp on tp.id_p = lot.protocol_id
	join equipment e on e.id_l = tp.id_eq
where lot.status is null