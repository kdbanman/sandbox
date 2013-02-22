-- for every customer...
select username
from Customer c
where exists (
  select *
  from Friend f1
  where (f1.user1 != 'c1' or f1.user2 != 'c1')
  and (f1.user1 = c.username or f1.user2 = c.username)
  and not exists (
    select *
    from Friend f2
    where (f2.user1 = 'c1' or f2.user2 = 'c1')
    and (f2.user1 = f1.user1
      or f2.user1 = f1.user2
      or f2.user2 = f1.user1
      or f2.user2 = f1.user2)
      )
    )
