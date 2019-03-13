import sys
from src.standard import Standard

class Modes:
  BLOCK_LEN = 32

  def __init__(self, key):
    self.cipher = Standard(key)

  def pad(self, bytes):
    pad_len = self.BLOCK_LEN - (len(bytes) % self.BLOCK_LEN) if len(bytes) % self.BLOCK_LEN else 0
    return bytes.ljust(len(bytes) + pad_len, b'\x00')

  def xor(self, byte_1, byte_2):
    int_a, int_b = int.from_bytes(byte_1, sys.byteorder), int.from_bytes(byte_2, sys.byteorder)
    result_xor = int_a ^ int_b
    return result_xor.to_bytes(len(byte_1), sys.byteorder)
  
class ECB(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, blocks):
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      blocks[index:index+self.BLOCK_LEN] = self.cipher.encrypt(blocks[index:index + self.BLOCK_LEN])
    return blocks
    
  def decrypt(self, blocks):
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      blocks[index:index+self.BLOCK_LEN] = self.cipher.decrypt(blocks[index:index + self.BLOCK_LEN])
    return blocks

class CBC(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, blocks, init_vector):
    temp = init_vector
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
      blocks[index:index+self.BLOCK_LEN] = self.cipher.encrypt(blocks[index:index + self.BLOCK_LEN])
      temp = blocks[index:index+self.BLOCK_LEN]
    return blocks
    
  def decrypt(self, blocks, init_vector):
    temp = init_vector
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp_cipher = blocks[index:index+self.BLOCK_LEN]
      blocks[index:index+self.BLOCK_LEN] = self.cipher.decrypt(blocks[index:index + self.BLOCK_LEN])
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
      temp = temp_cipher
    return blocks

class CFB(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, blocks, init_vector):
    temp = init_vector
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], self.cipher.encrypt(temp))
      temp = blocks[index:index+self.BLOCK_LEN]
    return blocks
    
  def decrypt(self, blocks, init_vector):
    temp = init_vector
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp_cipher = blocks[index:index+self.BLOCK_LEN]
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], self.cipher.encrypt(temp))
      temp = temp_cipher
    return blocks

class OFB(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, blocks, init_vector):
    temp = init_vector
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp = self.cipher.encrypt(temp)
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
    return blocks
    
  def decrypt(self, blocks, init_vector):
    temp = init_vector
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp = self.cipher.encrypt(temp)
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
    return blocks

class CTR(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, blocks, init_vector):
    temp = init_vector
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp = self.cipher.encrypt(temp)
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
    return blocks
    
  def decrypt(self, blocks, init_vector):
    temp = init_vector
    blocks = super().pad(blocks)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp = self.cipher.encrypt(temp)
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
    return blocks