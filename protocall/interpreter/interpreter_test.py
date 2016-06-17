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
"""Tests for protocall.runtime.runtime."""

import unittest

from google.protobuf import text_format

from protocall.proto import protocall_pb2
from protocall.runtime.vm import Protocall
from protocall.runtime import dump

from protocall.runtime.truth import true, false, literal_true, literal_false
from protocall.runtime.symbols import Symbols
from protocall.interpreter import grammar, parser_converter

def test_basic_code_test():
    s = """
{
  x=5;
  x=x+1;
  print_(x=x);
  return x;
}"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    return result

def test_basic_code_test():
    s = """
{
  x=5;
  x=x+1;
  print_(x=x);
  return x;
}"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    return result

def test_while_code_test():
    s = """
{
  x=5;
  print_(x=x);
  while (x > 0) {
    print_(x=x);
    x = x - 1;
  };
  print_(x=x);
  if (x>5) {
    print_(x=0);
  }
  elif (x<0) {
    print_(x=1);
  }
  else {
    print_(x=2);
  };
  return x;
}"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    return result

def test_function_code_test():
    s = """
{
  define f {
    print_(x=x);
    print_(y=y);
    return 0;
  };
  y=f(x=5,y=6);
  return 0;
}
"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    return result

def test_fibonacci_code_test():
    s = """
{
  define f {
    if (x == 0) {
      return 0;
    }
    elif (x == 1) {
      return 1;
    }
    else {
      a = f(x=x-2);
      b = f(x=x-1);
      return a+b;
    };
  };
  return f(x=5);
}
"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    return result

def test_factorial_code_test():
    s = """
{
  define factorial {
    if (x==0)
    {
      return 1;
    }
    else
    {
      return x * factorial(x=x-1);
    };
  };
  return factorial(x=12);
}

"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    print "Result=", result
    return result

def test_define_code_test():
    s = """
{
  define f {
    x = x - 1;
    print_(x=x);
    return x;
  };
  x = 5;
  print_(x=x);
  f(x=x);
  while (x>0) {
    print_(x=x);
    x = x - 1;
  };
  return x;
}
"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    print "Result=", result
    return result

def test_array_code_test():
    s = """
{
  x = 2;
  a = {5,6,x+5};
  print_symbols();
  print_(a=a);
  b=a[0];
  print_(b=b);
  b=a[1];
  print_(b=b);
  b=a[2];
  print_(b=b);
  return a[0];
}
"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    print "Result=", result
    return result

def test_array_append_code_test():
    # want to return a[3] at end but that causes exception
    s = """
{
  x = 2;
  a = {5, 6, 7};
  print_(a=a);
  a[0] = 6;
  print_(a=a);
  append(a=a, v=5);
  print_(a=a);
  return x;
}
"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    print "Result=", result
    return result

def test_proto_code_test():
    # want to return a[3] at end but that causes exception
    s = """
{
  x = Person<id: 7 name: "Bar" email: "bar@foo.com">;
  print_(id=x.id);
  return x.id;
}
"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    print "Result=", result
    return result

def test_proto_assignment_code_test():
    # want to return x.person.id at end but that causes exception
    s = """
{
  x = Person<id: 7 name: "Bar" email: "bar@foo.com">;
  x.id = 6;
  x.name = "Foo";
  x.person = Person<id: 17 name: "Bar" email: "bar@foo.com">;
  return 0;
}
"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    print "Result=", result
    return result

def test_proto_while_code_test():
    s = """
{
  x = Integer<value: 0>;
  print_(x=x);
  x.value = x.value + 1;
  print_(x=x);

  x = Integer<value: 5>;
  print_(value=x.value);
  while (x.value > 0) {
    print_(value=x.value);
    x.value = x.value - 1;
  };
  print_(value=x.value);
  if (x.value>5) {
    s = String<value: "0">;
    print_(s=s);
  }
  elif (x<0) {
    s = String<value: "1">;
    print_(s=s);
  }
  else {
    s = String<value: "2">;
    print_(s=s);
  };
  return x;

}
"""

def test_factorial_code_test():
    s = """
{
  define factorial {

    if (x.value==0)
    {
      return 1;
    }
    else
    {
      y= x.value * factorial(x=x.value-1);
      return y;
    };
  };
  x = Integer<value: 12>;
  y = factorial(x=x);
  return y;
}

"""
    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    print "Result=", result
    return result

    pr = Protocall()
    result = grammar.scope.parseString(s)
    sc = parser_converter.convert_scope(result[0].scope)
    result = pr.execute(sc.block)
    print "Result=", result
    return result


class InterpreterTest(unittest.TestCase):
  # def testBasicCodeTest(self):
  #   assert test_basic_code_test().atom.literal.integer.value == 6
  # def testWhileCodeTest(self):
  #   assert test_while_code_test().atom.literal.integer.value == 0
  # def testFunctionCodeTest(self):
  #   assert test_function_code_test().atom.literal.integer.value == 0
  # def testFibonacciCodeTest(self):
  #   assert test_fibonacci_code_test().atom.literal.integer.value == 5
  # def testFactorialCodeTest(self):
  #   assert test_factorial_code_test().atom.literal.integer.value == 479001600
  # def testDefineCodeTest(self):
  #   assert test_define_code_test().atom.literal.integer.value == 0
  # def testArrayCodeTest(self):
  #   assert test_array_code_test().atom.literal.integer.value == 5
  # def testArrayAppendCodeTest(self):
  #   assert test_array_append_code_test().atom.literal.integer.value == 2
  # def testProtoCodeTest(self):
  #   assert test_proto_code_test().atom.literal.integer.value == 7
  # def testProtoAssignmentCodeTest(self):
  #   assert test_proto_assignment_code_test().atom.literal.integer.value == 0
  # def testProtoOperatorCodeTest(self):
  #   assert test_proto_while_code_test().atom.literal.integer.value == 0
  def testProtoOperatorCodeTest(self):
    assert test_factorial_code_test().atom.literal.integer.value == 479001600


if __name__ == '__main__':
  unittest.main()
