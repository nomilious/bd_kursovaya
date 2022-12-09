Select
    user_id,
    user_group
from
    internal_user
where login="$login"
    and password="$password"
UNION ALL
Select
    user_id,
    NULL as user_group
from
    external_user
where login="$login"
    and password="$password"