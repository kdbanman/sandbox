create view MoviePopularity
as select m.mid, count(*) popularity
from Customer c, Movie m
where c.username in (
  (select username
  from Buy
  where m.mid = mediaid)
  union
  (select username
  from Rent
  where m.mid = movieid)
  )
group by m.mid;