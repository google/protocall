

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

class Type:
  def __init__(self, type_):
    self.type_ = type_

  def __getitem__(self, item):
    if item == 0:
      return self.type_
    else:
      raise IndexError

  def __repr__(self):
    return str(self.type_)

class Qualifier:
  def __init__(self, qualifier):
    self.qualifier = qualifier

  def __getitem__(self, item):
    if item == 0:
      return self.qualifier
    else:
      raise IndexError

  def __repr__(self):
    return str(self.qualifier)

class MessageBody:
  def __init__(self, body):
    self.body = []
    for line in body:
      self.body.append(line)

  def __getitem__(self, item):
    if item == 0:
      return self.body
    else:
      raise IndexError

  def __repr__(self):
    return "; ".join([str(line) for line in self.body]) + "; "

class MessageLine:
  def __init__(self, line):
    self.line = line

  def __getitem__(self, item):
    if item == 0:
      return self.line
    else:
      raise IndexError

  def __repr__(self):
    return str(self.line)

class MessageDefinition:
  def __init__(self, identifier, message_body):
    self.identifier = identifier
    self.message_body = message_body

  def __getitem__(self, item):
    if item == 0:
      return self.identifier
    elif item == 1:
      return self.message_body
    else:
      raise IndexError

  def __repr__(self):
    return "message " + str(self.identifier) + " { " + str(self.message_body) + "}"

class OneOfDefinition:
  def __init__(self, definition):
    self.definition = definition

  def __getitem__(self, item):
    if item == 0:
      return self.definition
    else:
      raise IndexError

  def __repr__(self):
    return str(self.definition)

class MethodDefinition:
  def __init__(self, definition):
    self.definition = definition

  def __getitem__(self, item):
    if item == 0:
      return self.definition
    else:
      raise IndexError

  def __repr__(self):
    return str(self.definition)

class PackageDirective:
  def __init__(self, directive):
    self.directive = directive

  def __getitem__(self, item):
    if item == 0:
      return self.directive
    else:
      raise IndexError

  def __repr__(self):
    return str(self.directive)

class ImportDirective:
  def __init__(self, directive):
    self.directive = directive

  def __getitem__(self, item):
    if item == 0:
      return self.directive
    else:
      raise IndexError

  def __repr__(self):
    return str(self.directive)

class Field:
  def __init__(self, qualifier, type_, identifier, integer):
    self.qualifier = qualifier
    self.type_ = type_
    self.identifier = identifier
    self.integer = integer

  def __getitem__(self, item):
    if item == 0:
      return self.qualifier
    if item == 1:
      return self.type_
    if item == 2:
      return self.identifier
    if item == 3:
      return self.integer
    else:
      raise IndexError

  def __repr__(self):
    return "%s %s %s = %s" % (self.qualifier, self.type_, self.identifier, self.integer)

class TopLevelStatement:
  def __init__(self, statement):
    self.statement = statement

  def __getitem__(self, item):
    if item == 0:
      return self.statement
    else:
      raise IndexError

  def __repr__(self):
    return str(self.statement)

class Parser:
  def __init__(self, parse):
    self.parse = parse

  def __getitem__(self, item):
    if item == 0:
      return self.parse
    else:
      raise IndexError

  def __repr__(self):
    return str(self.parse)
