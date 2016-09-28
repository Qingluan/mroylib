from fabric.api import local
try:
    from bson import ObjectId
except ImportError as e:
    from bson import objectid as ObjectId
try:
    import time
    from QmongoHelper import Mongo
except ImportError as e:
    import sys
    print("you should install QmongoHelper from my Github", file=sys.stderr)

from redis import Redis

DB_NAME = 'local'


class Singleton(object):

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kargs)
        return cls._instance



def db_add(doc, **data):
    db = Mongo(DB_NAME)
    db.insert(doc, **data)


def db_delete_one(_id, doc):
    db = Mongo(DB_NAME)
    return db.remove(doc, **{'_id':ObjectId(_id)})


def db_delete(_ids, doc):
    for _id in _ids:
        yield db_delete_one(_id, doc)


def db_search(info, doc, mon=None, year=None):
    if mon == None:
        mon = time.gmtime(time.time()).tm_mon
    db = Mongo(DB_NAME)
    res = db.find(doc, **{'time.year':year})
    if res == None:
        return []
    for i in res:
        if str(i).find(info) != -1 :
            yield i


def db_update(id, doc, **new):
    db = Mongo(DB_NAME)
    kargs = dict(**new)
    print({
            '$set':kargs
        })
    return db.update(doc, {'_id': ObjectId(id),},
        **{
            '$set':kargs
        })



class GotRedis(Singleton):

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.host = "{ip}:{port}".format(ip=host, port=port)
        self.redis = Redis(host=host, port=port, db=db)

    def __call__(self, *args):
        if len(args) == 1:
            return self.redis.get(args[0])
        elif len(args) == 2:
            return self.redis.set(*args)
        elif len(args) == 3:
            return self.redis.hset(*args)

    def __add__(self, *key):
        if len(key) == 1:
            return self.redis.incr(key[0])
        elif len(key) == 2:
            return self.redis.sadd(*key)
        elif len(key) == 3:
            return self.redis.hincrby(*key)
        else:
            err("incr or  sadd or hincrby can be supported")
            return False

    def __getitem__(self, key):
        return self.redis.smembers(key)

    def __setitem__(self, member_p, member_c):
        return self.redis.sadd(member_p, member_c)

    def keys(self):
        return self.redis.keys()

def upload():
    local("cd ~/RMDB && git branch")
    args = input("db_name > ").split()
    db_name_pre, db_name = args if len(args) ==2 else ['',args[0]]
    local("cd ~/RMDB && git checkout %s %s && ./package.sh c && git add -A && git commit -m \"upload %s  \" && git push origin %s -f " % (db_name_pre ,db_name ,time.asctime(), db_name))


def load():
    local("cd ~/RMDB && git branch")
    args = input("db_name > ").split()
    db_name_pre, db_name = args if len(args) ==2 else ['',args[0]]
    local("cd ~/RMDB && git checkout %s %s && git pull origin %s &&  ./package.sh d  " % (db_name_pre, db_name,db_name))    


