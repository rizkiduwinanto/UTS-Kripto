import src.modes as Modes

if __name__ == "__main__":
  key = b'argarg3r9i2p9tuslernsbgaeiga4tq2'
  mode = Modes.ECB(key)
  mode.decrypt('data/rinaldi.jpg')