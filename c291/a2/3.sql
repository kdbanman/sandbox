-- assumption 1: we are considering media purchases of customers other than
-- 'c1' regardless of their visibility setting
-- assupmtion 2: 'select distinct' counts as non-specified processing, so
-- duplicate entries are not removed from output

select b1.username
from Buy b1
where not exists (

    (select b2.mediaid
    from Buy b2
    where b2.username = 'c1' and b2.visibility = 'F')

    minus
    
    (select b3.mediaid
    from Buy b3
    where b3.username = b1.username)
);