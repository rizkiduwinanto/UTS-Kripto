import itertools
import random
import sys
import scipy
import base64
from src.utils import Sbox

class Standard:
  BLOCK_LENGTH = 256
  BYTE_LENGTH = 8
  BYTE_SIZE = 256
  HALF_BLOCK_LENGTH = BLOCK_LENGTH // 2
  HALF_BLOCK_BYTE_COUNT = HALF_BLOCK_LENGTH // BYTE_LENGTH
  ROUND_COUNT = 20

  def __init__(self, key):
    self.round_key = self.change_key(key)

  def transformation_function(self, key):
    pass

  def permutation_function(self, key):
    pass

  def round_function(self, half_block, key):
    pass

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
      left, right = right, bytes(c ^ d for c, d in zip(left, right))
    return left + right

  def decrypt(self, block):
    left, right = block[:self.HALF_BLOCK_BYTE_COUNT], block[self.HALF_BLOCK_BYTE_COUNT:]
    for index in reversed(range(self.ROUND_COUNT)):
      left, right = bytes(c ^ d for c, d in zip(left, right)), left
    return left + right

if __name__ == "__main__":
  key = 'KOMUNISCHINA'
  standard = Standard(key)
  standard.encrypt('data/rinaldi.jpg')

