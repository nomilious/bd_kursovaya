SELECT
	eq_id,
    title,
    protocol_id,
    status
FROM REPORTS_EQUIPMENT
	join REPORT_DATES on report_date_id = REPORT_DATES.id
where year = "$in_year"
	and month = "$in_month"