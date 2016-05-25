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

def value(literal):
    if isinstance(literal, protocall_pb2.Expression) and literal.HasField("atom"):
        return value(literal.atom.literal)
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("arithmetic_operator"):
        return literal.arithmetic_operator
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("comparison_operator"):
        return literal.comparison_operator
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("expression"):
        return literal.expression
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("integer"):
        return literal.integer.value
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("string"):
        return literal.string.value
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("array"):
        return '[ ' + ", ".join([str(value(element)) for element in literal.array.element]) + ' ]'
    elif isinstance(literal, protocall_pb2.Atom):
        return value(literal.literal)
    else:
        print literal.__class__
        import pdb; pdb.set_trace()
        raise RuntimeError
