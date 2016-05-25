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
from value import value

def print_(arguments, symbols):
    for arg in arguments:
        name = arg[0]
        atom = arg[1]
        print "%s: %s" % (name, value(atom))
    print
    return None

def double(arguments, symbols):
    arg = arguments[0]
    name = arg[0]
    atom = arg[1]
    
    a = protocall_pb2.Atom()
    a.literal.integer.value = atom.literal.integer.value * 2
    return a

def append(arguments, symbols):
  list_ = arguments[0]
  item = arguments[1]
  e = list_[1].literal.array.element.add()
  e.atom.CopyFrom(item[1])
  return e
