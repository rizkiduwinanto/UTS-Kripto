def make_bit_mask(length):
  return (1 << length) - 1

def bit_addition(b1, b2, length):
  return (b1 << length) + b2

def get_bits(number, length, offset=0):
  return (number >> offset) & make_bit_mask(length)

def concat_bits(length, *numbers):
  number = numbers[0]
  for i in range(1, len(numbers)):
    number = (number << length) | numbers[i]
  return number

def rotate_bits_left(number, length, count):
  return (number << count | number >> (length - count)) & make_bit_mask(length)

def rotate_bits_right(number, length, count):
  return (number >> count | number << (length - count)) & make_bit_mask(length)

def split_bits(number, length, count):
  return (get_bits(number, length, i * length) for i in reversed(range(count)))