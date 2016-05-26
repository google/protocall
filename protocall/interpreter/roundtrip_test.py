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
"""Tests for protocall.interpreter.roundtrip."""

import unittest

from pyparsing import ParseResults
from protocall.interpreter import parser_converter

from protocall.interpreter.grammar import scope
from protocall.runtime.vm import Protocall


class RoundtripTest(unittest.TestCase):


  def testRoundtrip(self):
    program = """{
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
    }
    """

    result = scope.parseString(program)
    print result[0]
    roundtrip = scope.parseString(repr(result[0]))
    print roundtrip[0]

    proto = parser_converter.convert_scope(result[0].scope)
    print proto
    pr = Protocall()
    pr.execute(proto.block)


if __name__ == '__main__':
  unittest.main()
