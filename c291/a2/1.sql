-- assumption:  the users are not in the WaitingList relation in order of
-- who is 'first,' so the results must be ordered to find who has been
-- waiting the longest.

select c.username, c.email
from Customer c, Media m, WaitingList w
where c.username = w.username
and w.movieid = m.id
and m.title = 'M3'
and w.since = (
  select min(w1.since)
  from WaitingList w1, Media m1
  where w1.movieid = m1.id
  and m1.title = 'M3'
  );