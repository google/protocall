from protocall.proto.parser import test_pb2

t = test_pb2.Person()
t.id = 5
t.name = "Foo"
t.email = "foo@foo.com"
t2 = test_pb2.Person()
t2.id = 7
t2.name = "Bar"
t2.email = "bar@foo.com"
t.person.CopyFrom(t2)

print str(t)
print str(t2)
