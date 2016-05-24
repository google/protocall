py_test(
    name = "runtime_test",
    srcs = ["runtime_test.py"],
    deps = [
        ":protocall",
        "//testing/pybase",
    ],
)

py_library(
    name = "protocall",
    srcs = [
        "builtins.py",
        "dump.py",
        "operators.py",
        "protocall.py",
        "subrs.py",
        "symbols.py",
        "truth.py",
        "value.py",
    ],
    deps = [
        "//experimental/users/dek/protocall/proto:protocall_proto_pb2",
        "//net/proto",
    ],
)
