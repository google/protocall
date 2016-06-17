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
from protocall.proto import types_pb2
from protocall.proto import test_pb2
from google.protobuf import text_format

# TODO dek: add API to register types, so test types and UDT can be registered at runtime.

protos = {
  'Person': test_pb2.Person,
  'Integer': types_pb2.Integer,
  'String': types_pb2.String,
}

def parse_proto(text, message_name):
  if message_name in protos:
    p = protos[message_name]()
    text_format.Merge(text, p)
    return p
  import pdb; pdb.set_trace()
  raise RuntimeError("message name is: '" + message_name + "'")
