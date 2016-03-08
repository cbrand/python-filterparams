# Python Filterparams #

Filterparams is a library for parsing URL paramters for filter
purposes in a backend. It provides a syntax to map SQL-like 
queries on top of the query parameters and parses it into a
python object.

This is a helper library for providing filter collection APIs. 
The primary use case for developing the library is to
use it with a REST-API which uses the [JSONAPI](http://jsonapi.org/) 
standard. Because of this the syntax is completely compatible with 
the standard and encapsulates everything in the `filter` query 
parameter.

## Installation ##

The package is available on [PyPi](https://pypi.python.org/pypi/filterparams).
You can install it through

```
pip install filterparams
```

The library was tested and should work with Python 2.7 and every 
Python 3 release. It was also tested to be compatible with pypy
and pypy3.

## Example ##

Given the URL (non URL escaped for better readability):
```
/users?filter[param][name][like][no_brand_name]=doe&filter[param][first_name]=doe%&filter[binding]=(!no_brand_name&first_name)&filter[order]=name&filter[order]=desc(first_name)
```

It can be parsed by the given function:

```python
from urllib.parse import urlsplit, parse_qs
from filterparams import build_parser

url = urlsplit(
    '/users?filter[param][name][like][no_brand_name]=doe'
    '&filter[param][first_name]=doe%&filter[binding]='
    '(!no_brand_name%26first_name)&filter[order]=name'
    '&filter[order]=desc(first_name)'
)
params = parse_qs(url.query)

valid_filters = ['eq', 'like']
default_filter = 'eq'

parser = build_parser(
    valid_filters=valid_filters,
    default_filter=default_filter,
)

query = parser(params)
```

Would parse the data. You can access the parsed filters through
`.param_order` and the orders through `.orders`. The param order
in this specific case would be resolved to:

```python
And(
    left=Parameter(
        name='name',
        alias='no_default_name',
        filter='like',
        value='doe%',
    ),
    right=Parameter(
        name='first_name',
        alias='first_name',
        filter='eq',
        value='doe',
    )
)
```

The orders would be:

```python
[Order(name='name', direction='asc'), 
 Order(name='first_name', direction='desc')]
```

## Syntax ##

All arguments must be prefixed by "filter". It is possible to 
query for specific data with filters, apply orders to the result 
and to combine filters through AND, NOT and OR bindings.

The syntax builds under the filter parameter a virtual object. 
The keys of the object are simulated through specifying `[{key}]` 
in the passed query parameter. Thus `filter[param]` would point 
to the param key in the filter object.

### Filter specification ###

The solution supports to query data through the `param` subkey.

```
filter[param][{parameter_name}][{operation}][{alias}] = {to_query_value}
```

The `operation` and `alias` parameters may be omitted. If no 
`alias` is provided the given parameter name is used for it.
If no `operation` is given, the default one is used (in the 
example this would be equal).

Example:
```
filter[param][phone_number][like]=001%
```

This would add a filter to all phone numbers which start with "001".

### Filter binding ###

Per default all filters are combined through AND clauses. 
You can change that by specifying the `filter[binding]` argument.

This is where the aliases which you can define come into place. 
The binding provides means to combine filters with AND and OR. 
Also you are able to negate filters here.

The filters are addressed by their alias or name, if no alias is 
provided.

If you have a filter `search_for_name`, `search_for_phone_number` 
and `search_for_account_number` defined you can say 
`search_for_name OR NOT search_for_number AND search_for_account_number` 
by specifying the following filter:

```
filter[binding]=search_for_name|(!search_for_phone_number&search_for_account_number)
```

Even though the brackets are useless here, you can use them in 
more complex filters.

The following table summarizes the possible configuration options:
<table>
  <thead>
    <tr>
      <th>Type</th>
      <th>Symbol</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>AND</td>
      <td>&</td>
      <td>a&b</td>
    </tr>
    <tr>
      <td>OR</td>
      <td>|</td>
      <td>a|b</td>
    </tr>
    <tr>
      <td>NOT</td>
      <td>!</td>
      <td>!a</td>
    </tr>
    <tr>
      <td>Bracket</td>
      <td>()</td>
      <td>(a|b)&c</td>
    </tr>
  </tbody>
</table>

### Ordering ###

To specify a sort order of the results the `filter[order]` parameter 
may be used. The value can be specified multiple times. To add 
ordering you have to provide the name of the parameter which should 
be ordered, not its alias!

If you want to order by `name`, `first_name` and in reverse order 
`balance` you can do so by specifying the following query url 
parameters:

```
filter[order]=name&filter[order]=first_name&filter[order]=desc(balance)
```

As you can see the `desc()` definition can be used to indicate 
reverse ordering.

### Filter definition ###

Not every backend does or should support all possible filter 
mechanisms. This is why the filters which should be accepted 
by the backend have to be added before processing the query 
parameters.

You can limit the allowed filters by building a parse through the
`filterparams.build_parser` function. You can configure the allowed
filters through the `valid_filters` definition. Additionally you
have to add the default filter by using the second `default_filter`
parameter.

```python
from filterparams import build_parser

valid_filters = ['eq', 'like']
default_filter = 'eq'

parser = build_parser(
    valid_filters=valid_filters,
    default_filter=default_filter,
)

query = parser({})
```

If you don't want any validation you can use the `parse` function.

```python
from filterparams import parse

query = parse({})
```

## Notes ##

- There do no yet exist any public projects which use this library to provide transparent mapping to an underlying 
backend. I plan long-term to add another library which does use this package and provide a way to map it on sqlalchemy models. 
If you are planning to do this or use it for other data mapping please contact me and I'll add a reference to it in
the README.
- The same as mentioned above is valid for client libraries, which generate the filter query structure in any language. 
Again, as soon as the API is stable I'll probably add a JavaScript library.
- Depending on your backend it might not make sense to support all features (ordering, parameter binding) of the
language. You might still want to use it to parse your basic parameters though and ignore the rest.

## License ##

The project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Used Libraries ##

For evaluating the filter params ordering the [funcparserlib](https://github.com/vlasovskikh/funcparserlib) ([MIT license](https://github.com/vlasovskikh/funcparserlib/blob/master/LICENSE))
module is used. Additionally the [Werkzeug](https://github.com/mitsuhiko/werkzeug) ([BSD license](https://github.com/mitsuhiko/werkzeug/blob/master/LICENSE)) package is used for supporting dicts with multiple values in the same key.

## Bindings ##

At the moment there does only exist a binding for mapping the filter
language on top of SQLAlchemy's declarative models. Other ones will
be added to the list if they become available:

- [sqlalchemy-filterparams](https://github.com/cbrand/python-sqlalchemy-filterparams) - Mapper for [SQLAlchemy](http://www.sqlalchemy.org/) declarative models.

## Other Languages ##

This is a list of projects implementing the same API for other languages.
Currently this list only has one entry.
 
- Go - [go-filterparams](https://github.com/cbrand/go-filterparams)
- Ruby - [filterparams](https://github.com/cbrand/ruby-filterparams)
- JavaScript (Client) - [filterparams](https://github.com/cbrand/js-filterparams-client)
