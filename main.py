import src.modes as Modes

def read_file(input_path):
  with open(input_path, "rb") as file:
    file_byte = file.read()
  extension = input_path.split('.').pop()
  return bytearray(file_byte), extension

def write_file(output_path, extension, file_byte):
  with open(output_path + '.' + extension, "wb") as file:
    file.write(file_byte)

if __name__ == "__main__":
  key = b'rizkiduwinantolulusjuli2019hehe'
  init_vector = b'rizkiduwinantolulusjuli2019hehe'
  filename = 'data/test.txt'
  name, extension = filename.split('.')

  mode = Modes.ECB(key)
  bytes, extension = read_file(filename)
  bytes_processed = mode.encrypt(bytes)
  write_file(name + 'ECB', extension, bytes_processed)
  bytes, extension = read_file(name + 'ECB.' + extension)
  bytes_processed = mode.decrypt(bytes)
  write_file(name + 'ECB_decrypted', extension, bytes_processed)

  mode = Modes.CBC(key)
  bytes, extension = read_file(filename)
  bytes_processed = mode.encrypt(bytes, init_vector)
  write_file(name + 'CBC', extension, bytes_processed)
  bytes, extension = read_file(name + 'CBC.' + extension)
  bytes_processed = mode.decrypt(bytes, init_vector)
  write_file(name + 'CBC_decrypted', extension, bytes_processed)

  mode = Modes.CFB(key)
  bytes, extension = read_file(filename)
  bytes_processed = mode.encrypt(bytes, init_vector)
  write_file(name + 'CFB', extension, bytes_processed)
  bytes, extension = read_file(name + 'CFB.' + extension)
  bytes_processed = mode.decrypt(bytes, init_vector)
  write_file(name + 'CFB_decrypted', extension, bytes_processed)

  mode = Modes.OFB(key)
  bytes, extension = read_file(filename)
  bytes_processed = mode.encrypt(bytes, init_vector)
  write_file(name + 'OFB', extension, bytes_processed)
  bytes, extension = read_file(name + 'OFB.' + extension)
  bytes_processed = mode.decrypt(bytes, init_vector)
  write_file(name + 'OFB_decrypted', extension, bytes_processed)
