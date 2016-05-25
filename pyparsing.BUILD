genrule(
    name = "copy_pyparsing",
    srcs = ["pyparsing-2.1.4/pyparsing.py"],
    outs = ["pyparsing.py"],
    cmd = "cp $< $(@)",
)

py_library(
    name = "pyparsing",
    srcs = ["pyparsing.py"],
    visibility = ["//visibility:public"],
    srcs_version = "PY2AND3",
)
