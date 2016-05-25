#py_test(
#    name = "runtime_test",
#    srcs = ["runtime_test.py"],
#    deps = [
#        ":protocall",
#        "//testing/pybase",
#    ],
#)

py_library(
    name = "protocall",
    srcs = [
        "builtins.py",
        "dump.py",
        "operators.py",
        "subrs.py",
        "symbols.py",
        "truth.py",
        "value.py",
        "vm.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        # "//net/proto",
        # "//google/proto",
        "//protocall/proto:protocall_proto_pb2",
    ],
)
