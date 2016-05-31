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
load("//google/protobuf:protobuf.bzl", "py_proto_library")

py_proto_library(
    name = "protocall_proto_pb2",
    srcs = ["protocall.proto"],
    default_runtime = "//google/protobuf:protobuf_python",
    protoc = "//google/protobuf:protoc",
    visibility = ["//visibility:public"],
)

py_proto_library(
    name = "test_proto_pb2",
    srcs = ["test.proto"],
    default_runtime = "//google/protobuf:protobuf_python",
    protoc = "//google/protobuf:protoc",
    visibility = ["//visibility:public"],
)

py_proto_library(
    name = "types_proto_pb2",
    srcs = ["types.proto"],
    default_runtime = "//google/protobuf:protobuf_python",
    protoc = "//google/protobuf:protoc",
    visibility = ["//visibility:public"],
)
