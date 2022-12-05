from typing import List, Sequence
def to_decimal(base: int, base_number: Sequence[int]) -> int:
  '''
  Given the base (eg: 2) and the base_number (eg: [1, 0, 1, 1]),
  return the decimal representation (in this case, answer should be 11).
  '''
  result = 0
  n = 1

  for digit in reversed(base_number):
    result += digit * n
    n *= base

  return result

def from_decimal(base: int, decimal_number: int) -> Sequence[int]:
  '''
  Given the base (eg: 2) and the decimal_number (eg: 11),
  return the base representation (in this case, answer should be [1, 0, 1, 1])
  '''
  result = []
  while decimal_number > 0:
    result.append(decimal_number % base)
    decimal_number //= base

  return list(reversed(result))

if __name__ == '__main__':
  base: int = 7
  base_number: Sequence[int] = [5, 1, 6, 0, 3, 6, 2]
  print(f"Given number in base {base:d} is {base_number}")
  decimal_number: int = to_decimal(base, base_number)
  print(f"Converted decimal number is {decimal_number}")
  base_number_recover: Sequence[int] = from_decimal(base, decimal_number)
  print(f"Recovered number in base {base:d} is {base_number_recover}")
  correct: bool = base_number == base_number_recover
  print(f"Is the code working correctly? {correct}")
