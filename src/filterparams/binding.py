# -*- encoding: utf-8 -*-
# pylint: disable=too-many-locals,unnecessary-lambda,undefined-variable

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


def tokenize(to_tokenize_str):
    specs = [
        ('Space', (r'[ \t\r\n]+',)),
        ('Word', (r'[\w\-\_]+',)),
        ('Op', (r'[\\(\\)\\|\\!\\&]{1}',)),
    ]
    useless = [u'Space']
    tokenizer = make_tokenizer(specs)
    return [
        token
        for token in tokenizer(to_tokenize_str)
        if token.type not in useless
    ]


def parse(sequence, query):
    tokval = lambda x: x.value
    toktype = lambda t: (
        some(lambda x: x.type == t).named('(type %s)' % t) >> tokval
    )
    operation = lambda s: a(Token('Op', s)) >> tokval
    operation_ = lambda s: skip(operation(s))

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
    bracket = operation_('(') + inner_bracket + operation_(')')
    and_ = left_of_and + operation_('&') + right_of_and >> make_and
    or_ = left_of_or + operation_('|') + inner_bracket >> make_or
    param = word >> create_param

    not_.define(operation_('!') + (bracket | param))
    not_ = not_ >> make_not

    left_of_or.define(and_ | bracket | not_ | param)
    left_of_and.define(bracket | not_ | param)
    right_of_and.define(left_of_and)
    inner_bracket.define(or_ | and_ | bracket | not_ | param)

    definition = (bracket | inner_bracket) + finished

    return definition.parse(sequence)


def loads(to_parse_string, query):
    return parse(tokenize(to_parse_string), query)
