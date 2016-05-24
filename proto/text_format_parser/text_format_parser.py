from protocall.proto.text_format_parser.AST import Integer, Identifier, Data, TopLevelDefinition, Nested, Parser
from pyparsing import Word, alphas, alphanums, Regex, Suppress, Forward, Group, oneOf, ZeroOrMore, Optional, delimitedList, Keyword, restOfLine, dblQuotedString

def identifier_fn(s,l,t):
  return Identifier(t[0])
def integer_fn(s,l,t):
  return Integer(int(t[0]))
def data_fn(s,l,t):
  return Data(t[0])
def top_level_definition_fn(s,l,t):
  return TopLevelDefinition(t[0], t[1])
def nested_fn(s,l,t):
  return Nested(t[0], t[1])
def parser_fn(s,l,t):
  return Parser(t)


integer = Regex(r"[+-]?\d+")
integer.setParseAction(integer_fn)

LBRACE = Suppress('{')
RBRACE = Suppress('}')
COLON = Suppress(':')

identifier = Word(alphas+"_",alphanums+"_")
identifier.setParseAction(identifier_fn)

data = integer | dblQuotedString
data.setParseAction(data_fn)

top_level_definition = identifier + COLON + data
top_level_definition.setParseAction(top_level_definition_fn)

nested = Forward()
nested.setParseAction(nested_fn)
parser = ZeroOrMore(top_level_definition | nested)
parser.setParseAction(parser_fn)

nested << identifier + LBRACE + parser + RBRACE

# test_string = """id: 5
# name: "Foo"
# email: "foo@foo.com"
# person {
#   id: 7
#   name: "Bar"
#   email: "bar@foo.com"
# }
# """
# x = parser.parseString(test_string, parseAll=True)
# print x[0]
# import pdb; pdb.set_trace()
