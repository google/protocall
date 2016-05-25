# Copyright 2016 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from google.protobuf import text_format
import sys
from protocall.proto import test_pb2
from protocall.proto.text_format_parser import text_format_parser

from pyparsing import Word, alphas, alphanums, Regex, Suppress, Forward, Group, oneOf, ZeroOrMore, Optional, delimitedList, Keyword, restOfLine, dblQuotedString, nums

PRINT = Keyword('print')
SET = Keyword('set')

EQ = Suppress('=');
IDENTIFIER = Word(alphas+"_",alphanums+"_")
FIELD = delimitedList(IDENTIFIER, '.', combine=False)("field")
PRINT_FIELD = PRINT + FIELD

INTEGER = Word(nums)("integer")
STRING = dblQuotedString("string")
TRUE = Keyword("true")
FALSE = Keyword("false")
BOOLEAN = (TRUE | FALSE)("boolean")
TEXT_PROTO = text_format_parser.parser("proto")
VALUE = (INTEGER | STRING | BOOLEAN | TEXT_PROTO)("value")

SET_FIELD_VALUE = SET + FIELD + EQ + VALUE
STATEMENT = (PRINT_FIELD | SET_FIELD_VALUE)

def visit_node(protos, field):
  parent = None
  var = protos[field[0]]
  if len(field):
    for f in field[1:]:
      if hasattr(var, f):
        parent = var
        var = getattr(var, f)
      else:
        raise RuntimeError("var %s does not have field %s" % (type(var), f))
  return parent, f

if len(sys.argv) == 1:
  t = test_pb2.Person()
  t.id = 0
  t.name = "dek"
  t.email = "dek"
  protos = {'t': t}


  while True:
    line = raw_input('> ')
    print "line=", line
    result = STATEMENT.parseString(line)
    if result[0] == "print":
      field = result[1:]
      print "print field", field
      var = protos[field[0]]
      if len(field):
        for f in field[1:]:
          if hasattr(var, f):
            var = getattr(var, f)
          else:
            print "var", type(var), "does not have field", f
            break
      print "var=", type(var)
      print var
    elif result[0] == "set":
      field = result[1:-1]
      value = result[-1]
      if 'integer' in result.keys():
        print "set integer field", field, "to value", value
        node, f = visit_node(protos, field)
        setattr(node, f, int(value))
      elif 'boolean' in result.keys():
        print "set boolean field", field, "to value", value
        node, f = visit_node(protos, field)
        setattr(node, ff, bool(value))
      elif 'string' in result.keys():
        print "set string field", field, "to value", value
        node, f = visit_node(protos, field)
        setattr(node, f, value)
      elif 'proto' in result.keys():
        print "set proto field", field, "to value", value
        node, f = visit_node(protos, field)
        f2 = getattr(node, f)
        f3 = f2.__class__()
        s = str(value)
        text_format.Parse(s, f3)
        f2.CopyFrom(f3)
        import pdb; pdb.set_trace()
      else:
        raise RuntimeError(result.keys())
    else:
      raise RuntimeError(line)
