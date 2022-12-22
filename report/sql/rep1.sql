SELECT
	staff_id,
    FIO,
    proto_closed,
    tests_done
FROM REPORTS_STAFF
	join REPORT_DATES on report_date_id = REPORT_DATES.id
where year = "$in_year"
	and month = "$in_month"