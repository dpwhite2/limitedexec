import collections

Traits = collections.namedtuple('Traits','name category non_expr description')
T = Traits

node_traits = [
    T('Module','mod',False,''),
    T('Interactive','mod',False,''),
    T('Expression','mod',False,''),
    
    T('FunctionDef','stmt',True,'function definition statement'),
    T('ClassDef','stmt',True,'class definition statement'),
    T('Return','stmt',True,'return statement'),
    T('Delete','stmt',True,'delete statement'),
    T('Assign','stmt',True,'assignment statement'),
    T('AugAssign','stmt',True,'augmented assignment statement'),
    T('Print','stmt',True,'print statement'),
    T('For','stmt',True,'for statement'),
    T('While','stmt',True,'while statement'),
    T('If','stmt',True,'if statement'),
    T('With','stmt',True,'with statement'),
    T('Raise','stmt',True,'raise statement'),
    T('TryExcept','stmt',True,'try..except statement'),
    T('TryFinally','stmt',True,'try..finally statement'),
    T('Assert','stmt',True,'assert statement'),
    T('Import','stmt',True,'import statement'),
    T('ImportFrom','stmt',True,'import..from statement'),
    T('Exec','stmt',True,'exec statement'),
    T('Global','stmt',True,'global statement'),
    T('Nonlocal','stmt',True,'nonlocal statement'),
    T('Expr','stmt',False,'expression statement'),
    T('Pass','stmt',True,'pass statement'),
    T('Break','stmt',True,'break statement'),
    T('Continue','stmt',True,'continue statement'),
    
    T('BoolOp','expr',False,'boolean operator expression'),
    T('BinOp','expr',False,'binary operator expression'),
    T('UnaryOp','expr',False,'unary operator expression'),
    T('Lambda','expr',False,'lambda expression'),
    T('IfExpr','expr',False,'if expression'),
    T('Dict','expr',False,'dict expression'),
    T('Set','expr',False,'set expression'),
    T('ListComp','expr',False,'list comprehension expression'),
    T('SetComp','expr',False,'set comprehension expression'),
    T('DictComp','expr',False,'dict comprehension expression'),
    T('GeneratorExp','expr',False,'generator expression'),
    T('Yield','expr',False,'yield expression'),
    T('Compare','expr',False,'compare expression'),
    T('Call','expr',False,'call expression'),
    T('Repr','expr',False,'repr expression'),
    T('Num','expr',False,'number'),
    T('Str','expr',False,'string'),
    T('Bytes','expr',False,'bytes'),
    T('Ellipsis','expr',False,'ellipsis'),
    T('Attribute','expr',False,'attribute expression'),
    T('Subscript','expr',False,'subscript expression'),
    T('Name','expr',False,'identifier'),
    T('List','expr',False,'list expression'),
    T('Tuple','expr',False,'tuple expression'),
    
    T('Load','expr_context',False,''),
    T('Store','expr_context',False,''),
    T('Del','expr_context',False,''),
    T('AugLoad','expr_context',False,''),
    T('AugStore','expr_context',False,''),
    T('Param','expr_context',False,''),
    
    T('Ellipsis','slice',False,'ellipsis'),
    T('Slice','slice',False,'slice'),
    T('ExtSlice','slice',False,'extended slice'),
    T('Index','slice',False,''),
    
    T('And','boolop',False,''),
    T('Or','boolop',False,''),
    T('Add','operator',False,''),
    T('Sub','operator',False,''),
    T('Mult','operator',False,''),
    T('Div','operator',False,''),
    T('Mod','operator',False,''),
    T('Pow','operator',False,''),
    T('LShift','operator',False,''),
    T('RShift','operator',False,''),
    T('BitOr','operator',False,''),
    T('BitTrueor','operator',False,''),
    T('BitAnd','operator',False,''),
    T('FloorDiv','operator',False,''),
    T('Invert','unaryop',False,''),
    T('Not','unaryop',False,''),
    T('UAdd','unaryop',False,''),
    T('USub','unaryop',False,''),
    T('Eq','cmpop',False,''),
    T('NotEq','cmpop',False,''),
    T('Lt','cmpop',False,''),
    T('LtE','cmpop',False,''),
    T('Gt','cmpop',False,''),
    T('GtE','cmpop',False,''),
    T('Is','cmpop',False,''),
    T('IsNot','cmpop',False,''),
    T('In','cmpop',False,''),
    T('NotIn','cmpop',False,''),
    
    T('ExceptionHandler','excepthandler',False,'exception handler'),
]

node_traits = dict((t.name, t) for t in node_traits)

del T





