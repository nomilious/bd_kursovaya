select cnt, cnt_null from
(select count(*) as cnt_null  from list_of_testing where protocol_id = "$id" and status is NULL) a,
(select count(*) as cnt from list_of_testing where protocol_id = "$id") b