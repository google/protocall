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

    def add_local_symbol(self, key, value):
        self.stack[-1][key] = value

    def lookup(self, key):
#        print "searching", key, "in", self.dump()
        for i in range(len(self.stack), 0, -1):
            if key in self.stack[i-1]:
                return self.stack[i-1][key]
        raise KeyError, key

    def lookup_local(self, key):
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
