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
py_library(
    name = "parser",
    srcs = [
        "AST.py",
        "grammar.py",
    ],
    deps = [
        "//external:pyparsing",
        "//protocall/proto/text_format_parser",
    ],
)

py_library(
    name = "parser_converter",
    srcs = [
        "parser_converter.py",
    ],
    deps = [
        "//protocall/proto:protocall_proto_pb2",
    ],
)

py_binary(
    name = "interpreter",
    srcs = [
        "interpreter.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        ":parser",
        ":parser_converter",
        "//protocall/proto:protocall_proto_pb2",
        "//protocall/runtime:protocall",
    ],
)

py_test(
    name = "parser_test",
    srcs = ["parser_test.py"],
    deps = [
        ":parser",
        ":parser_converter",
    ],
)

py_test(
    name = "roundtrip_test",
    srcs = ["roundtrip_test.py"],
    deps = [
        ":parser",
        ":parser_converter",
        "//protocall/runtime:protocall",
    ],
)
