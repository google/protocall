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
py_binary(
    name = "generate_text",
    srcs = ["generate_text.py"],
    deps = [
        "//protocall/proto:test_proto_pb2",
    ],
)

py_library(
    name = "AST",
    srcs = ["AST.py"],
    deps = [
    ],
)

py_library(
    name = "text_format_parser",
    srcs = ["text_format_parser.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":AST",
        # "//third_party/py/pyparsing",
    ],
)
