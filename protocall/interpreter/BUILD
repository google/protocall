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
    deps = [
        ":parser",
        ":parser_converter",
        "//protocall/proto:protocall_proto_pb2",
        "//protocall/runtime:protocall",
        # "//third_party/py/readline",
    ],
)

# py_test(
#     name = "parser_test",
#     srcs = ["parser_test.py"],
#     deps = [
#         ":parser",
#         ":parser_converter",
#         "//testing/pybase",
#     ],
# )

# py_test(
#     name = "roundtrip_test",
#     srcs = ["roundtrip_test.py"],
#     deps = [
#         ":parser",
#         ":parser_converter",
#         "//protocallruntime:protocall",
#         "//testing/pybase",
#     ],
# )
