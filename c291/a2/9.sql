select mov.genre, med.title
from Media med, Movie mov, MoviePopularity mp
where med.id = mov.mid 
and mp.mid = mov.mid
and mp.popularity >= all (
    select  mp1.popularity
    from Movie mov1, MoviePopularity mp1
    where mov1.mid = mp1.mid
    and mov.genre = mov1.genre
);
