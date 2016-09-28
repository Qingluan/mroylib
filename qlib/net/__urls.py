

def gen_urls(f, default="http://"):
    with open(f) as fp:
        for line in fp:
            t = check_uri(line, default)
            if t:
                yield t


def check_uri(line, default="http://"):
    l = line.strip()
    if len(l.split()) != 1:
        return False

    if not l.startswith(default):
        return default + l
    else:
        return l

def url_to_db(db, url):
    rs = re.findall(r'(?:http\://.+?)(/.+)', url)
    if rs:
        db.insert("urls",**{"uri":rs[0]})
