"""Tests for protocall.interpreter.roundtrip."""

import googletest

from pyparsing import ParseResults
from protocall.interpreter import parser_converter

from protocall.interpreter.grammar import scope
from protocall.runtime import protocall


class RoundtripTest(googletest.TestCase):


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
    pr = protocall.Protocall()
    pr.execute(proto.block)


if __name__ == '__main__':
  googletest.main()
