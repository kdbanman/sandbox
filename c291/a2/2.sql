-- assumption: a friend relationship between person1 and person2 may be
-- in the Friend table with user1 = 'person1' and user2 = 'person2' or as
-- user1 = 'person2' and user2 = 'person1'

(select user2
from Friend
where user1 = 'c1')

union

(select user1
from Friend
where user2 = 'c1');
