protocall is an experimental Google programming language.  The purpose of
protocall is to explore a number of programming approaches with the goal of
making distributed systems easier to develop.

Protocall adopts a number of philosophical principles:

0) Simplicity, Flexibility, and Experimentation are the primary goals of
protocall.  Performance is a non-goal.

1) Protocall programs are expressed using Google Protocol Buffers.  Entire
programs, statements, identifiers, and types are all represented using a simple
protocall schema.  Programs and all data can be serialized, deserialized, and
manipulated using the protocol buffer API outside of the language.

2) The Protocall runtime is a simple VM that executes protocall protocol
buffers.

3) While simple, the language contains primitive types, arrays, structured
types, variables, conditionals, loops and functions.  Structured types in
protocall can be any protocol buffer type.  This includes the protocall protocol
buffer schema, making programs that write programs (or modify themselves)
trivial.

4) Calls to remote services that speak protocol buffers over gRPC are especially
simple: they look just like function calls that take Request arguments and
return a Response.  Similarly, implementing gRPC services that speak protocol
buffers is also trivial.

5) The language delegates nearly all additional functionality to external
libraries- the standard library is a collection of external libraries, with a
small syntactic sugar layer on top.  Making calls to foreign functions is
trivial.

6) Because writing programs directly in protocol buffers is tedious, protocall
provides an interpreter (with a REPL).  The interpreted language, SeeThruP0,
resembles Python and LISP and transliterates to protocall.  Rather than
attempting to make the protocall language include more features (such as
syntactic sugar), users are encouraged to implement the language functionality
at the interpreted level, and implement the runtime functionality as libraries in the
protocall VM.

A simple SeeThruP0 session looks like this.  Lines starting with "#" are
commentary about what is happening.  Lines starting with "> " are user commands.
The interpreter prints the result of evaluating each line.

# Assign the integer value 5 to the identifier 'x'
> x = 5;
literal {
  integer {
    value: 5
  }
}

# Call the function "print_", with the value of the identifier 'x' in this scope
# bound to a local variable 'x' within the function.  The print_ function returns None.
> print_(x=x);
x: 5

None

The assignment statement above is expressed in protocall as:

statement {
  assignment {
    identifier {
      name: "x"
    }
    expression {
      atom {
        literal {
          integer {
            value: 5
          }
        }
      }
    }
  }
}

The print statement is expressed in protocall as:

statement {
  call {
    identifier {
      name: "print_"
    }
    argument {
      identifier {
        name: "x"
      }
      expression {
        atom {
          identifier {
            name: "x"
          }
        }
      }
    }
  }
}

A simple SeeThruP0 program with a loop.
{
  x=5;
  while (x > 0) {
    print_(x=x);
    x = x - 1;
  };
}

A simple program to compute Fibonacci numbers.  This demonstates scoping,
function definition and conditionals.
{
  define f {
    if (x == 0) {
      return 0;
    }
    elif (x == 1) {
      return 1;
    }
    else {
      a = f(x=x-2);
      b = f(x=x-1);
      return a+b;
    };
  };
  return f(x=5);
}

SeeThruP0 uses { and } for scoping- program, function and conditional body.
Each scope induces a new local variable space.  Argument are passed to function
by copy; use return values to communicate.






TODO(dek):
 documentation
 proto type/assignment support
 better proto type support (various ints)
 FFI support
 RPC support
 namespaces
 interpreter multi-line support
 imports of other files
 
