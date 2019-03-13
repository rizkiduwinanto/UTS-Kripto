import itertools
import random
import sys
import scipy.fftpack as scp
import numpy
import src.bit_operation as bit_operation

class Standard:
  BLOCK_LENGTH = 256
  BYTE_LENGTH = 8
  BYTE_SIZE = 256
  HALF_BLOCK_LENGTH = BLOCK_LENGTH // 2
  HALF_BLOCK_BYTE_COUNT = HALF_BLOCK_LENGTH // BYTE_LENGTH
  ROUND_COUNT = 20

  SHIFT_ROWS = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0X9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF]
  OUTER_CLOCKWISE = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB]
  INNER_CLOCKWISE = [0xC, 0xD, 0xE, 0xF]


  def __init__(self, key):
    random.seed(key)
    self.Sbox = [[random.randrange(0, self.BYTE_SIZE) for _ in range(0, self.BYTE_SIZE)] for _ in range(0, self.HALF_BLOCK_BYTE_COUNT)]
    
    Pbox1 = list(random.sample(range(self.HALF_BLOCK_BYTE_COUNT), self.HALF_BLOCK_BYTE_COUNT) for _ in range(self.BYTE_LENGTH))
    Pbox2 = list(random.sample(range(self.BYTE_LENGTH), self.BYTE_LENGTH) for _ in range(self.HALF_BLOCK_BYTE_COUNT))
    self.Pbox = [None for _ in range(self.HALF_BLOCK_LENGTH)]
    for i in range(self.HALF_BLOCK_BYTE_COUNT):
      for j in range(self.BYTE_LENGTH):
        self.Pbox[Pbox1[j][i] * self.BYTE_LENGTH + j] = Pbox2[i][j] * self.HALF_BLOCK_BYTE_COUNT + i

    self.round_key = self.change_key(key)

  def mix_block_key(self, half_block, key):
    return bytes(c ^ d for c, d in zip(half_block, key))

  def subtitute(self, half_block):
    return bytes(self.Sbox[i][c] for i, c in enumerate(half_block))
  
  def shift_rows(self, half_block):
    return bytes(half_block[i] for i in self.SHIFT_ROWS)

  def reversed_shift_rows(self, half_block):
    return bytes(half_block[i] for i in reversed(self.SHIFT_ROWS))

  def rotate_right(self, half_block, count):
    return bytes(bit_operation.rotate_bits_right(x, self.BYTE_LENGTH, count%self.BYTE_LENGTH) for x in half_block)

  def rotate_left(self, half_block, count):
    return bytes(bit_operation.rotate_bits_left(x, self.BYTE_LENGTH, count%self.BYTE_LENGTH) for x in half_block)

  def circular_rotation(self, half_block, count):
    return bytes(half_block[i] for _, i in sorted(itertools.chain(zip(self.OUTER_CLOCKWISE, self.OUTER_CLOCKWISE[count:] + self.OUTER_CLOCKWISE[:count]), zip(self.INNER_CLOCKWISE, self.INNER_CLOCKWISE[count:] + self.INNER_CLOCKWISE[:count]))))

  def cosine_transform(self, half_block):
    int_half_block = [int.from_bytes(half_block, sys.byteorder)]
    return bytes(scp.dct(int_half_block))
  
  def fourier_transform(self, half_block):
    int_half_block = [int.from_bytes(half_block, sys.byteorder)]
    return bytes(scp.fft(int_half_block))

  def transform(self, half_block, key):
    temp = [half_block]
    for bytes_key in key:
      count = bit_operation.get_bits(bytes_key, 4, 0)
      token = bit_operation.get_bits(bytes_key, 4, 4)
      count = -count if token < 8 else count
      temp = self.rotate_left(half_block, count) if token < 8 else self.rotate_right(half_block, count)
      for i in range(abs(count)):
        temp = self.shift_rows(temp) if token < 8 else self.shift_rows(temp)
        temp = self.circular_rotation(temp, count)
      temp = self.circular_rotation(temp, count)
      temp = self.cosine_transform(temp) if token < 8 else self.fourier_transform(temp)
    return temp

  def permutate(self, half_block):
    return int.to_bytes(bit_operation.concat_bits(1, *(x for _, x in sorted(zip(self.Pbox, bit_operation.split_bits(int.from_bytes(half_block, sys.byteorder), 1, self.HALF_BLOCK_LENGTH))))), self.HALF_BLOCK_BYTE_COUNT, sys.byteorder)

  def round_function(self, half_block, key):
    return self.permutate(self.transform(self.subtitute(self.mix_block_key(half_block, key)), key))

  def change_key(self, key):
    round_keys = []
    for index in range(len(key) // self.HALF_BLOCK_BYTE_COUNT):
      round_keys.append(key[index * self.HALF_BLOCK_BYTE_COUNT:(index + 1) * self.HALF_BLOCK_BYTE_COUNT])
    for i in range(self.ROUND_COUNT):
      round_keys.append(self.round_function(round_keys[i], round_keys[-1]))
    return round_keys[-self.ROUND_COUNT:]
  
  def encrypt(self, block):
    left, right = block[:self.HALF_BLOCK_BYTE_COUNT], block[self.HALF_BLOCK_BYTE_COUNT:]
    for index in range(self.ROUND_COUNT):
      left, right = right, bytes(c ^ d for c, d in zip(left, self.round_function(right, self.round_key[index])))
    return left + right

  def decrypt(self, block):
    left, right = block[:self.HALF_BLOCK_BYTE_COUNT], block[self.HALF_BLOCK_BYTE_COUNT:]
    for index in reversed(range(self.ROUND_COUNT)):
      left, right = bytes(c ^ d for c, d in zip(right, self.round_function(left, self.round_key[index]))), left
    return left + right

