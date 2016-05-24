def setq(protocall, arguments, symbols):
    identifier = arguments[0].expression.atom.identifier
    expression = arguments[1].expression
    e = protocall.evaluate(expression)
    symbols.add_global_symbol(identifier.name, e)
    return e

def print_symbols(protocall, arguments, symbols):
    print "Symbols:"
    print symbols.dump()
    return None
