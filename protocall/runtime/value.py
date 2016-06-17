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
from protocall.proto import protocall_pb2
from google.protobuf import message
def value(literal):
    if isinstance(literal, protocall_pb2.Expression) and literal.HasField("atom"):
        result = value(literal.atom.literal)
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("arithmetic_operator"):
        result = literal.arithmetic_operator
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("comparison_operator"):
        result =  literal.comparison_operator
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("expression"):
        result = literal.expression
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("integer"):
        result = literal.integer.value
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("string"):
        result = literal.string.value
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("array"):
        result = '[ ' + ", ".join([str(value(element)) for element in literal.array.element]) + ' ]'
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("proto"):
        print "XXX"
        print "literal:", literal
        result = literal.proto
    elif isinstance(literal, protocall_pb2.Atom):
        result = value(literal.literal)
    elif isinstance(literal, int):
        result = literal
    elif isinstance(literal, str):
        result = literal
    elif isinstance(literal, unicode):
        result = literal
    elif isinstance(literal, float):
        result = literal
    elif isinstance(literal, message.Message):
        print "YYY"
        result = literal
    elif isinstance(literal, None):
        print "Warning: None value."
        result = None
    else:
        print literal.__class__
        import pdb; pdb.set_trace()
        raise RuntimeError
    return result
