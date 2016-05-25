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
"""Tests for protocall.interpreter.parser."""

import googletest


from pyparsing import ParseResults
from protocall.interpreter import parser_converter

from protocall.interpreter.grammar import expression, statement, assignment, call, return_expression, block, scope, define_function_scope, while_scope, if_scope, elif_scope, elif_scopes, else_scope, conditional


class ParserTest(googletest.TestCase):

  def testExpression(self):
    result = expression.parseString("(4 / x) - 2 > 5")
    assert str(result[0]) == "(((4 / x) - 2) > 5)"

  def testAssignment(self):
    result = assignment.parseString("x = 4 / y - 2 > 5")
    assert str(result[0]) == "x = ((4 / (y - 2)) > 5)"

  def testCall(self):
    result = call.parseString("print_(x=x + 5,y=y)")
    assert str(result[0]) == "print_(x = (x + 5),y = y)"

  def testReturn(self):
    result = return_expression.parseString("return (x + 5)")
    assert str(result[0]) == "return (x + 5)"

  def testIfScope(self):
    result = if_scope.parseString("if (x < 5) { return y; }")
    assert str(result[0]) == "if ((x < 5)) { return y; }"

  def testElifScope(self):
    result = elif_scope.parseString("elif (x < 5) { return y; }")
    assert str(result[0]) == "elif ((x < 5)) { return y; }"

  def testElifScopes(self):
    result = elif_scopes.parseString("elif (x < 5) { return y; } elif (x > 5) { return z; }")
    assert str(result[0]) == "elif ((x < 5)) { return y; } elif ((x > 5)) { return z; }"

  def testElseScope(self):
    result = else_scope.parseString("else { return y; }")
    assert str(result[0]) == "else { return y; }"

  def testConditional(self):
    result = conditional.parseString("if (x < 5) { return y; } elif (x > 9) { return z; } elif (x > 5) { return a; } else { return c; }")
    assert str(result[0]) == "if ((x < 5)) { return y; } elif ((x > 9)) { return z; } elif ((x > 5)) { return a; } else { return c; }"

  def testConditional2(self):
    result = conditional.parseString("if (x < 5) { return y; } elif (x > 9) { return z; }")
    assert str(result[0]) == "if ((x < 5)) { return y; } elif ((x > 9)) { return z; }"

  def testConditional3(self):
    result = conditional.parseString("if (x < 5) { return y; } else { return c; }")
    assert str(result[0]) == "if ((x < 5)) { return y; }  else { return c; }"

  def testWhileScope(self):
    result = while_scope.parseString("while (x < 5) { return y; }")
    assert str(result[0]) == "while ((x < 5)) { return y; }"

  def testStatement(self):
    result = statement.parseString("return x + 5;")
    assert str(result[0]) == "return (x + 5);"

  def testBlock(self):
    result = block.parseString("x=x + 5; return x + 5;")
    assert str(result[0]) == "x = (x + 5); return (x + 5);"

  def testScope(self):
    result = scope.parseString("{ print_(x=x + 5); return x + 5; }")
    assert str(result[0]) == "{ print_(x = (x + 5)); return (x + 5); }"

  def testDefine(self):
    result = define_function_scope.parseString("define f { print_(x=x); }")
    assert str(result[0]) == "define f { print_(x = x); }"


if __name__ == '__main__':
  googletest.main()
