workspace(name = "com_google")
bind(
    name = "python_headers",
    actual = "//:dummy",
)

new_http_archive(
    name = "six_archive",
    url = "https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz#md5=34eed507548117b2ab523ab14b2f8b55",
    sha256 = "105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a",
    build_file = "six.BUILD",
)
bind(
    name = "six",
    actual = "@six_archive//:six",
)

new_http_archive(
    name = "pyparsing_archive",
    url = "https://pypi.python.org/packages/ae/0c/b6ce7eea7ccf020ae68db1119bacaa07ad91fedaefaf8f3265e8dd156813/pyparsing-2.1.4.tar.gz#md5=322059c57f0c9f11da1c6c06a2ba2197",
    sha256 = "a9234dea79b50d49b92a994132cd1c84e873f3936db94977a66f0a4159b1797c",
    build_file = "pyparsing.BUILD",
)

bind(
    name = "pyparsing",
    actual = "@pyparsing_archive//:pyparsing",
)
