select artistid
from Fan
where since > '01-SEP-12'
group by artistid
having count(*) >= all (
  select count(*)
  from Fan
  where since > '01-SEP-12'
  group by artistid
  );