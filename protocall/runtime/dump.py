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
from protocall.proto import protocall_pb2

def field_to_string(field):
    return ".".join([component.name for component in field.component])

def dump_expression(expression):
    if expression.HasField("atom"):
        atom = expression.atom
        if atom.HasField("literal"):
            literal = atom.literal
            if literal.HasField("integer"):
                s = str(literal.integer.value)
            elif literal.HasField("string"):
                s = "'%s'" % literal.string.value
            elif literal.HasField("boolean"):
                if literal.boolean.value == False:
                    s = 'false'
                elif literal.boolean.value == True:
                    s = 'true'
            elif literal.HasField("array"):
                s = "'%s'" % literal.array.element
            else:
                raise RuntimeError
        elif atom.HasField("field"):
            s = field_to_string(atom.field)
        elif atom.HasField("expression"):
            expression2 = atom.expression
            s = dump_expression(expression2)
        else:
            raise RuntimeError
    elif expression.HasField("arithmetic_operator"):
        operator = expression.arithmetic_operator
        o = operator.operator
        if o == protocall_pb2.ArithmeticOperator.Op.Value("PLUS"):
            ostr = "+"
        elif o == protocall_pb2.ArithmeticOperator.Op.Value("MINUS"):
            ostr = "-"
        elif o == protocall_pb2.ArithmeticOperator.Op.Value("MULTIPLY"):
            ostr = "*"
        elif o == protocall_pb2.ArithmeticOperator.Op.Value("DIVIDE"):
            ostr = "/"
        else:
            raise RuntimeError
        left = dump_expression(operator.left)
        right = dump_expression(operator.right)
        s = "(%s %s %s)" % (left, ostr, right)
    elif expression.HasField("comparison_operator"):
        operator = expression.comparison_operator
        o = operator.operator
        if o == protocall_pb2.ComparisonOperator.Op.Value("EQUALS"):
            ostr = "=="
        elif o == protocall_pb2.ComparisonOperator.Op.Value("LESS_THAN"):
            ostr = "<"
        elif o == protocall_pb2.ComparisonOperator.Op.Value("GREATER_THAN"):
            ostr = ">"
        else:
            raise RuntimeError
        left = dump_expression(operator.left)
        right = dump_expression(operator.right)
        s = "(%s %s %s)" % (left, ostr, right)
    elif expression.HasField("call"):
        call = expression.call
        name = field_to_string(call.field)
        arguments = call.argument
        args = [ "%s=%s" % (arg.identifier.name, dump_expression(arg.expression)) for arg in arguments ]
        s = "%s(%s)" % (name, ",".join(args))
    else:
        raise RuntimeError
    return s

def indent(s, level=0):
    return '  ' * level + s

def dump(block, level=0):
    result = ["\n" + indent('{', level)]
    for statement in block.statement:
        if statement.HasField("assignment"):
            assignment = statement.assignment
            name = field_to_string(assignment.field)
            expression = dump_expression(assignment.expression)
            s = indent("%s = %s;" %  (name, expression), level+1)
        elif statement.HasField("call"):
            call = statement.call
            name = field_to_string(call.field)
            arguments = call.argument
            args = [ "%s=%s" % (arg.identifier.name, dump_expression(arg.expression)) for arg in arguments ]
            s = indent("%s(%s);" % (name, ",".join(args)), level+1)
        elif statement.HasField("conditional"):
            conditional = statement.conditional
            if_scope = conditional.if_scope
            s = indent("if %s%s" % (
                dump_expression(if_scope.expression),
                dump(conditional.if_scope.scope.block, level+1)),
                       level+1)
            for elif_scope in conditional.elif_scope:
                s += "\n" + indent("elif %s%s" % (dump_expression(elif_scope.expression), dump(elif_scope.scope.block, level+1)), level+1)
            if conditional.HasField("else_scope"):
                else_scope = conditional.else_scope
                s += "\n" + indent("else %s;" % (dump(conditional.else_scope.block, level+1)), level+1)
        elif statement.HasField("return_"):
            return_ = statement.return_
            s = indent("return %s;" % dump_expression(return_.expression), level+1)
        elif statement.HasField("while_"):
            while_ = statement.while_
            expression_scope = while_.expression_scope
            s = indent("while %s%s;" % (dump_expression(expression_scope.expression), dump(expression_scope.scope.block, level+1)), level+1)
        elif statement.HasField("define"):
            define = statement.define
            block = define.scope.block
            s = indent("define %s%s;" % (field_to_string(define.field), dump(block, level+1)), level+1)
        else:
            raise RuntimeError
        result.append(s)
    result.append(indent('}', level))
    return "\n".join([r for r in result] )
