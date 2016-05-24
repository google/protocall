py_binary(
    name = "generate_text",
    srcs = ["generate_text.py"],
    deps = [
        "//experimental/users/dek/protocall/proto:test_proto_pb2",
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
    deps = [
        ":AST",
        "//third_party/py/pyparsing",
    ],
)
