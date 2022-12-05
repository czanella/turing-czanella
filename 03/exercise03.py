def combinations(n):
  indexes = [0] * n

  while True:
    yield indexes
    i = 0
    while i < n and indexes[i] == 1:
      indexes[i] = 0
      i += 1
    if i == n:
      break
    else:
      indexes[i] = 1

def subsets_of_integers(integers):
  indexed_integers = list(enumerate(integers))
  for combination in combinations(len(indexed_integers)):
    yield tuple(v for (i, v) in indexed_integers if combination[i] == 1)

### Tests
if __name__ == '__main__':
  assert set(subsets_of_integers(range(5))) == {
    (),
    (0,),
    (1,),
    (2,),
    (3,),
    (4,),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
    (0, 1, 2),
    (0, 1, 3),
    (0, 1, 4),
    (0, 2, 3),
    (0, 2, 4),
    (0, 3, 4),
    (1, 2, 3),
    (1, 2, 4),
    (1, 3, 4),
    (2, 3, 4),
    (0, 1, 2, 3),
    (0, 1, 2, 4),
    (0, 1, 3, 4),
    (0, 2, 3, 4),
    (1, 2, 3, 4),
    (0, 1, 2, 3, 4),
  }, 'Should generate all subsets of integers'

  for n in range(1, 21):
    assert len(list(subsets_of_integers(range(n)))) == 2 ** n, 'Should generate all 2^n combinations'

  print('All assertions succeeded')


# NOTE: this exercise could be easily be completed using `itertools.combinations`:
# from itertools import combinations
#
# def subsets_of_integers(l):
#   for r in range(len(l)):
#     for c in combinations(l, r):
#       print(list(c))
#
# ... but I believe this would be cheating. :)