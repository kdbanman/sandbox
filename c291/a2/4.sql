select Rent.username, Rate.rating
from (Rent left outer join Rate on (Rent.movieid = Rate.movieid and Rent.username = Rate.username)), Media
where Media.id = Rent.movieid
and Media.title = 'M2'
and Rent.visibility = 'A';
