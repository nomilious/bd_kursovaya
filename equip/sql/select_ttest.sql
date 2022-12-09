with planed_but_not_done as (
    select tt.*
    from ttest_plan  tt
        left join list_of_testing t on tt.id_tt = t.id_ttest_date
    where id_ttest_date is null
        and date_tt  >= (
            select min(outt.date_t)
            from (select date_t from test_protocol where status is null) outt
        )
)
select  tp.id_p, tp.date_t, e.title, e.eq_t, outt.id_tt, outt.date_tt
from test_protocol tp
	left join list_of_testing  lot on tp.id_p = lot.protocol_id
	join equipment e on e.id_l = tp.id_eq
	join equipment_type et on et.id_t = e.eq_t
	join planed_but_not_done outt on outt.id_t = et.id_t
where lot.protocol_id is null
	and e.eq_t in (
		select distinct id_t
		from planed_but_not_done
	)