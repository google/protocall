

class Identifier:
  def __init__(self, identifier):
    self.identifier = identifier

  def __getitem__(self, item):
    if item == 0:
      return self.identifier
    else:
      raise IndexError

  def __repr__(self):
    return self.identifier

class Integer:
  def __init__(self, value):
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return str(self.value)

class Data:
  def __init__(self, value):
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return str(self.value)

class TopLevelDefinition:
  def __init__(self, identifier, data):
    self.identifier = identifier
    self.data = data

  def __getitem__(self, item):
    if item == 0:
      return self.identifier
    elif item == 1:
      return self.data
    else:
      raise IndexError

  def __repr__(self):
    return str("%s: %s" % (self.identifier, self.data))

class Nested:
  def __init__(self, identifier, parser):
    self.identifier = identifier
    self.parser = parser

  def __getitem__(self, item):
    if item == 0:
      return self.identifier
    if item == 1:
      return self.parser
    else:
      raise IndexError

  def __repr__(self):
    return "%s {\n%s\n}" % (self.identifier, self.parser)

class Parser:
  def __init__(self, values):
    self.values = values

  def __getitem__(self, item):
    if item == 0:
      return self.values
    else:
      raise IndexError

  def __repr__(self):
    return "\n".join(["%s" % value for value in self.values])
