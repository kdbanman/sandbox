-- assumption:  'select distinct' is non-specified processing of output, so
-- duplicate results are to be left in.

select m1.title
from Media m1, Song s1
where s1.albumid = m1.id
and m1.title != 'A1'
and s1.artistid in (
    select s2.artistid
    from Song s2, Media m2
    where m2.id = s2.albumid
    and m2.title = 'A1'
);