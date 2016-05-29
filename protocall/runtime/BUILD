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

py_test(
    name = "runtime_test",
    srcs = ["runtime_test.py"],
    deps = [
        ":protocall",
        "//protocall/interpreter",
    ],
)

py_library(
    name = "protocall",
    srcs = [
        "builtins.py",
        "dump.py",
        "operators.py",
        "protos.py",
        "subrs.py",
        "symbols.py",
        "truth.py",
        "value.py",
        "vm.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//protocall/proto:protocall_proto_pb2",
        "//protocall/proto:test_proto_pb2",
    ],
)
