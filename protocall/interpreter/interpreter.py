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
import sys

from protocall.proto import protocall_pb2
from google.protobuf import text_format
from protocall.interpreter import parser_converter
import readline
from protocall.runtime import dump
from pyparsing import ParseException
from protocall.interpreter.grammar import block, scope
from protocall.runtime import vm

pr = vm.Protocall()
# pr.enable_tracing()

if len(sys.argv) == 1:
  while True:
    try:
      line = raw_input('> ')
      try:
        print "line=", line
        result = block.parseString(line)
      except ParseException as e:
        print "Error parsing input at line", e.lineno, "column", e.col
        print e.line
        print ' ' * (e.col-2), '^'
        print e
      else:
        bl = parser_converter.convert_block(result[0])
        try:
          print pr.execute(bl)
        except Exception as e:
          print e
    except EOFError:
      break
else:
  filename = sys.argv[1]
  lines = open(filename).read()
  result = scope.parseString(lines)
  sc = parser_converter.convert_scope(result[0].scope)
  # print "dump"
  # s= dump.dump(sc.block)
  # print s
  # end-to-end parse of file, print as program, parse that.
  # result2 = scope.parseString(s)
  print pr.execute(sc.block)
