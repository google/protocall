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

from protos import parse_proto
from google.protobuf import text_format
from google.protobuf.message import Message

class Symbols:
    def __init__(self, initial=None):
        if not initial:
            initial = {}
        self.stack = [initial]

    def push_frame(self, symbols=None):
        if not symbols:
            symbols = {}
        self.stack.append(symbols)

    def pop_frame(self):
        return self.stack.pop()


    def add_symbol(self, key, value):
        for i in range(len(self.stack), 0, -1):
            if key in self.stack[i-1]:
                self.stack[i-1][key] = value
                return
        self.stack[-1][key] = value

    def add_global_symbol(self, key, value):
        self.stack[0][key] = value

    def traverse_atom(self, atom):
        value = atom.literal.proto.value
        field = ".".join([component.name for component in atom.literal.proto.field.component])
        base = parse_proto(value, field)
        p = base
        parent = None
        for component in atom.literal.proto.field.component:
            if hasattr(p, component.name):
                parent = p
                p = getattr(p, component.name)
            else:
                raise RuntimeError("did not find component %s in proto %s" % (component, p))
        return parent, base, p

    def add_local_symbol(self, field, value):
        if len(field.component) == 1:
          self.stack[-1][field.component[0].name] = value
        else:
          components = list(reversed([component.name for component in field.component]))
          print "components=", components
          try:
            atom = self.lookup_local_key(components.pop())
            parent, base, p = self.traverse_atom(atom)
          except:
            import pdb; pdb.set_trace()
          if isinstance(p, Message):
            result = parse_proto(value.literal.proto.value, value.literal.proto.field.component[0].name)
            getattr(parent, field.component[-1].name).CopyFrom(result)
            self.stack[-1][field.component[0].name].literal.proto.value = text_format.MessageToString(base)
          else:
            setattr(parent, field.component[-1].name, value)
            self.stack[-1][field.component[0].name].literal.proto.value = text_format.MessageToString(base)

    def lookup(self, field):
        if len(field.component) == 1:
          key = field.component[0].name
          return self.lookup_key(key)
        else:
          components = list(reversed([component.name for component in field.component]))
          atom = self.lookup_key(components.pop())
          parent, base, p = self.traverse_atom(atom)

        return p

    def lookup_key(self, key):
#        print "searching", key, "in", self.dump()
        for i in range(len(self.stack), 0, -1):
            if key in self.stack[i-1]:
                return self.stack[i-1][key]
        raise KeyError, key

    def lookup_local(self, field):
        if len(field.component) == 1:
          key = field.component[0].name
          return self.lookup_local_key(key)
        components = list(reversed([component.name for component in field.component]))
        atom = self.lookup_local_key(components.pop())
        parent, base, p = self.traverse_atom(atom)
        return p

    def lookup_local_key(self, key):
        return self.stack[-1][key]

    def locals(self):
        return self.stack[-1]

    def globals(self):
        d = {}
        for i in range(len(self.stack)):
            d.update(self.stack[i])
        return d

    def dump(self):
        for i in range(len(self.stack)):
            print i, self.stack[i]
