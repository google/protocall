from protocall.proto import protocall_pb2
from value import value

def print_(arguments, symbols):
    for arg in arguments:
        name = arg[0]
        atom = arg[1]
        print "%s: %s" % (name, value(atom))
    print
    return None

def double(arguments, symbols):
    arg = arguments[0]
    name = arg[0]
    atom = arg[1]
    
    a = protocall_pb2.Atom()
    a.literal.integer.value = atom.literal.integer.value * 2
    return a

def append(arguments, symbols):
  list_ = arguments[0]
  item = arguments[1]
  e = list_[1].literal.array.element.add()
  e.atom.CopyFrom(item[1])
  return e
