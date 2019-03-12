import sys
from src.standard import Standard

class Modes:
  BLOCK_LEN = 32

  def __init__(self, key):
    self.cipher = Standard(key)

  def xor(self, a, b):
    int_a, int_b = int.from_bytes(a, sys.byteorder), int.from_bytes(b, sys.byteorder)
    return (int_a ^ int_b).to_bytes(len(a), sys.byteorder)
  
  def read_file(self, input_path):
    with open(input_path, "rb") as file:
      file_byte = file.read()
    return bytearray(file_byte)

  def write_file(self, input_path, file_byte):
    with open(input_path, "wb") as file:
      file.write(file_byte)

class ECB(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, input_path):
    blocks = self.read_file(input_path)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      blocks[index:index+self.BLOCK_LEN] = self.cipher.encrypt(blocks[index:index + self.BLOCK_LEN])
    self.write_file(input_path, blocks)
    
  def decrypt(self, input_path):
    blocks = self.read_file(input_path)
    for index in range(0, len(blocks), self.BLOCK_LEN):
      blocks[index:index+self.BLOCK_LEN] = self.cipher.decrypt(blocks[index:index + self.BLOCK_LEN])
    self.write_file(input_path, blocks)

class CBC(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, input_path, init_vector):
    blocks = self.read_file(input_path)
    temp = init_vector
    for index in range(0, len(blocks), self.BLOCK_LEN):
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
      blocks[index:index+self.BLOCK_LEN] = self.cipher.encrypt(blocks[index:index + self.BLOCK_LEN])
      temp = blocks[index:index+self.BLOCK_LEN]
    self.write_file(input_path, blocks)
    
  def decrypt(self, input_path, init_vector):
    blocks = self.read_file(input_path)
    temp = init_vector
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp_cipher = blocks[index:index+self.BLOCK_LEN]
      blocks[index:index+self.BLOCK_LEN] = self.cipher.decrypt(blocks[index:index + self.BLOCK_LEN])
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
      temp = temp_cipher
    self.write_file(input_path, blocks)

class CFB(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, input_path, init_vector):
    blocks = self.read_file(input_path)
    temp = init_vector
    for index in range(0, len(blocks), self.BLOCK_LEN):
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], self.cipher.encrypt(temp))
      temp = blocks[index:index+self.BLOCK_LEN]
    self.write_file(input_path, blocks)
    
  def decrypt(self, input_path, init_vector):
    blocks = self.read_file(input_path)
    temp = init_vector
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp_cipher = blocks[index:index+self.BLOCK_LEN]
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], self.cipher.encrypt(temp))
      temp = temp_cipher
    self.write_file(input_path, blocks)

class OFB(Modes):
  def __init__(self, key):
    return super().__init__(key)

  def encrypt(self, input_path, init_vector):
    blocks = self.read_file(input_path)
    temp = init_vector
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp = self.cipher.encrypt(temp)
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
    self.write_file(input_path, blocks)
    
  def decrypt(self, input_path, init_vector):
    blocks = self.read_file(input_path)
    temp = init_vector
    for index in range(0, len(blocks), self.BLOCK_LEN):
      temp = self.cipher.encrypt(temp)
      blocks[index:index+self.BLOCK_LEN] = super().xor(blocks[index:index + self.BLOCK_LEN], temp)
    self.write_file(input_path, blocks)