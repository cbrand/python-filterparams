# -*- encoding: utf-8 -*-

from funcparserlib.lexer import (
    make_tokenizer,
    Token
)
from funcparserlib.parser import (
    a,
    skip,
    some,
    forward_decl,
    finished
)

from .obj import (
    And,
    Or,
    Not,
)


def tokenize(str):
    specs = [
        ('Space', (r'[ \t\r\n]+',)),
        ('Word', (r'[\w\-\_]+',)),
        ('Op', (r'[\\(\\)\\|\\!\\&]{1}',)),
    ]
    useless = [u'Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def parse(sequence, query):
    tokval = lambda x: x.value
    toktype = lambda t: (
        some(lambda x: x.type == t).named('(type %s)' % t) >> tokval
    )
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))

    create_param = lambda param_name: query.get_aliased_param(
            param_name
    )
    make_and = lambda params: And(params[0], params[1])
    make_or = lambda params: Or(params[0], params[1])
    make_not = lambda inner: Not(inner)

    word = toktype('Word')
    inner_bracket = forward_decl()
    left_of_and = forward_decl()
    right_of_and = forward_decl()
    left_of_or = forward_decl()
    not_ = forward_decl()
    bracket = op_('(') + inner_bracket + op_(')')
    and_ = left_of_and + op_('&') + right_of_and >> make_and
    or_ = left_of_or + op_('|') + inner_bracket >> make_or
    param = word >> create_param

    not_.define(op_('!') + (bracket | param))
    not_ = not_ >> make_not

    left_of_or.define(and_ | bracket | not_ | param)
    left_of_and.define(bracket | not_ | param)
    right_of_and.define(left_of_and)
    inner_bracket.define(or_ | and_ | bracket | not_ | param)

    definition = (bracket | inner_bracket) + finished

    return definition.parse(sequence)


def loads(s, query):
    return parse(tokenize(s), query)
