SELECT
	eq_id,
    title,
    status
FROM REPORTS_EQUIPMENT
	join REPORT_DATES on report_date_id = REPORT_DATES.id
where year = "$in_year"
	and month = "$in_month"
order by eq_id