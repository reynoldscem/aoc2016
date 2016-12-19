from itertools import count

num = 3001330

for a in count():
  if 2**(a + 1) >= num:
    print(2 * (num - 2**a) + 1)
    break
