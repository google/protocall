proto_library(
    name = "protocall_proto",
    srcs = ["protocall.proto"],
    has_services = 1,
    py_api_version = 2,
)

py_proto_library(
    name = "protocall_proto_pb2",
    api_version = 2,
    deps = ["protocall_proto"],
)

proto_library(
    name = "test_proto",
    srcs = ["test.proto"],
    has_services = 1,
    py_api_version = 2,
)

py_proto_library(
    name = "test_proto_pb2",
    api_version = 2,
    deps = ["test_proto"],
)
