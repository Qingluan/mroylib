import re


def extract(string, pre='(', back=')'):
    """
    Can extract content between from spic[0] and spic[1], default spic is '()' , which from string.
    """

    l_count = 0
    while string.find(pre) != -1:
        l_count += 1
        s = string.find(pre) + len(pre)
        string = string[s:]

        last_b = string.rfind(back)
        next_s = string.find(pre)
        next_b = string.find(back)
        if next_b < next_s:
            yield string[:next_b]
            string = string[next_b:] 
        else:
            yield string[:last_b]
            string = string[:last_b]


def get_from_func(string, name):

    while string.find(name) != -1:
        string = string[string.find(name) + len(name):]
        yield next(extract(string))


def get_from_tag(string, tag):
    pre='<%s>' % tag
    back = '</%s>' % tag
    while string.find(tag) != -1:
        yield next(extract(string, pre=pre, back=back))
        string = string[string.find(pre) + len(pre):]


def replace_tag_to(string, func=False, **tags):
    """
    relace tag's content to value in tags

    @func = False/True
        while set True , will use tags's value should pass callback function, not value

    """
    def _tag(tag):
        return '<%s>' % tag, '<%s/>' % tag

    for tag in tags:
        val = tags[tag]
        for raw in get_from_tag(string, tag):
            if not func:
                string = string.replace('<{tag}>{raw}</{tag}>'.format(tag=tag, raw=raw), val)
            else:
                string = string.replace('<{tag}>{raw}</{tag}>'.format(tag=tag, raw=raw), val(raw))

    return string