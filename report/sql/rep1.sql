SELECT
	staff_id,
    FIO,
    works_done,
    div_code,
    people_in_div,
    div_works
FROM REPORTS_STAFF
	join REPORT_DATES on report_date_id = REPORT_DATES.id
where year = "$in_year"
	and month = "$in_month"