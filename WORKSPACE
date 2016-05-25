workspace(name = "com_google")
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
bind(
    name = "python_headers",
    actual = "//:dummy",
)
