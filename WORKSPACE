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
