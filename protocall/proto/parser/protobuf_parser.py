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
from AST import Identifier, Integer, Type, Qualifier, MessageBody, MessageLine, MessageDefinition, OneOfDefinition, MethodDefinition, PackageDirective, ImportDirective, Field, TopLevelStatement, Parser
from pyparsing import Word, alphas, alphanums, Regex, Suppress, Forward, Group, oneOf, ZeroOrMore, Optional, delimitedList, Keyword, restOfLine, quotedString

def identifier_fn(s,l,t):
  return Identifier(t[0])
def integer_fn(s,l,t):
  return Integer(int(t[0]))
def type_fn(s,l,t):
  return Type(t[0])
def qualifier_fn(s,l,t):
  return Qualifier(t[0])
def message_definition_fn(s,l,t):
  return MessageDefinition(*t)
def oneof_definition_fn(s,l,t):
  return OneOfDefinition(t[0])
def message_body_fn(s,l,t):
  return MessageBody(t[0])
def message_line_fn(s,l,t):
  return MessageLine(t[0])
def method_definition_fn(s,l,t):
  return MethodDefinition(t[0])
def package_directive_fn(s,l,t):
  return PackageDirective(t[0])
def import_directive_fn(s,l,t):
  return ImportDirective(t[0])
def field_fn(s,l,t):
  return Field(*t)
def service_definition_fn(s,l,t):
  return ServiceDefintion(t[0])
def top_level_statement_fn(s,l,t):
  return TopLevelStatement(t[0])
def parser_fn(s,l,t):
  return Parser(t[0])

identifier = Word(alphas+"_",alphanums+"_").setName("identifier")
identifier.setParseAction(identifier_fn)

integer = Regex(r"[+-]?\d+")
integer.setParseAction(integer_fn)

LBRACE = Suppress('{')
RBRACE = Suppress('}')
LBRACK = Suppress('[')
RBRACK = Suppress(']')
LPAR = Suppress('(')
RPAR = Suppress(')')
EQ = Suppress('=');
SEMI = Suppress(';')

SYNTAX = Keyword('syntax')
IMPORT = Keyword('import')
PACKAGE = Keyword('package')
MESSAGE = Keyword('message')
RPC = Keyword('rpc')
RETURNS = Keyword('returns')
SERVICE = Keyword('service')
OPTION = Keyword('option')
ENUM = Keyword('enum')
ONEOF = Keyword('oneof')
REQUIRED = Keyword('required')
OPTIONAL = Keyword('optional')
REPEATED = Keyword('repeated')
TRUE = Keyword('true')
FALSE = Keyword('false')


message_body = Forward()

message_definition= Suppress(MESSAGE) - identifier("message_id") + Suppress(LBRACE) + message_body("message_body") + Suppress(RBRACE)
message_definition.setParseAction(message_definition_fn)
enum_definition= ENUM - identifier + LBRACE + ZeroOrMore(Group(identifier + EQ + integer + SEMI) ) + RBRACE

DOUBLE = Keyword("double")
INT32 = Keyword("int32")
UINT32 = Keyword("uint32")
BOOL = Keyword("bool")
STRING = Keyword("string")

type_ = (DOUBLE | UINT32 | BOOL | STRING | identifier)
type_.setParseAction(type_fn)
qualifier = (REQUIRED | OPTIONAL | REPEATED )("qualifier")
qualifier.setParseAction(qualifier_fn)
field = qualifier - type_("type_") + identifier("identifier") + EQ + integer("field_number") + SEMI
field.setParseAction(field_fn)

oneof_definition= ONEOF - identifier + LBRACE + ZeroOrMore(Group(type_("type_") + identifier("identifier") + EQ + integer("field_number") + SEMI) ) + RBRACE
oneof_definition.setParseAction(oneof_definition_fn)

message_line = (field | enum_definition| oneof_definition| message_definition)("message_line")
message_line.setParseAction(message_line_fn)

message_body << Group(ZeroOrMore(message_line))("message_body")
message_body.setParseAction(message_body_fn)

method_definition= ((RPC - identifier("method") +
              LPAR + Optional(identifier("request")) + RPAR +
              RETURNS + LPAR + Optional(identifier("response")) + RPAR))("method_definition")
method_definition.setParseAction(method_definition_fn)

service_definition= (SERVICE - identifier("service") + LBRACE + ZeroOrMore(Group(method_definition)) + RBRACE)("service_definition")
service_definition.setParseAction(service_definition_fn)

package_directive = (Group(PACKAGE - delimitedList(identifier, '.', combine=True) + SEMI))("package_directive")
package_directive.setParseAction(package_directive_fn)

import_directive = IMPORT - quotedString("import") + SEMI
import_directive.setParseAction(import_directive_fn)

option_directive = OPTION - identifier("option") + EQ + (integer | quotedString)("value") + SEMI

top_level_statement = Group(message_definition| enum_definition| option_directive | import_directive | service_definition)("top_level_statement")
top_level_statement.setParseAction(top_level_statement_fn)

syntax_directive = (SYNTAX + EQ + quotedString("syntax_version") + SEMI)("syntax_directive")

parser = (Optional(syntax_directive) + Optional(package_directive) + ZeroOrMore(top_level_statement))("parser")
parser.setParseAction(parser_fn)

comment = '//' + restOfLine
parser.ignore(comment)

test2 = """message Person {
  required uint32 id = 1;
  required string name = 2;
  optional string email = 3;
  optional Person person = 4;
}"""


from pprint import pprint
#~ print parser.parseString(test2, parseAll=True).dump()
x = parser.parseString(test2, parseAll=True)
statement = x.parser.statement[0]

print statement
import pdb; pdb.set_trace()
