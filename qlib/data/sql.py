import time
import datetime
from hashlib import sha256


def _hash(obj):
    return sha256(obj.encode('utf8')).hexdigest()



class SqlEngine:


    DEFAULT_TABLE = """CREATE TABLE %s (
        ID INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        CreatedTime TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP, 
        {extends} );"""

    def __init__(self,database=None, type='sqlite' , **connect_options):
        self.Type = type
        engine = None
        if not database and type == 'sqlite':
            type = 'mysql'
            self.Type = 'mysql'
            database = 'test'

        try:
            if type == 'sqlite':
                self.DEFAULT_TABLE = self.DEFAULT_TABLE.replace('AUTO_INCREMENT', '')
                import sqlite3
                engine = sqlite3
            elif type == 'mysql':
                import pymysql
                engine = pymysql
            elif type == 'postgresql':
                import psycopg2
                engine = psycopg2
            else:
                raise Exception("un supported sql: %s" % type)

        except ImportError as e:
            print(e)
        if self.Type == 'sqlite':
            self.con = engine.connect(database, **connect_options)
        else:

            self.con = engine.connect(database=database, **connect_options)
        self.cu = self.con.cursor()

    def got_datetime(timeobj):
        if isinstance(timeobj, datetime.datetime):
            return timeobj
        elif isinstance(timeobj, str):
            ss = time.strptime(timeobj, '%Y-%m-%d %H:%M:%S')
            return datetime.datetime.fromtimestamp(time.mktime(ss))

    def run_cmd(self, cmd, *values):
        try:
            if values:
                self.cu.execute(cmd, values)
            else:
                self.cu.execute(cmd)
        except Exception as e:
            print(e)
            print(values)
            print(cmd)
            raise e

        return self.con.commit()

    def create_table(self, table, *extends_columns):
        columns = ',\n\t'.join(extends_columns)
        cmd = self.DEFAULT_TABLE.format(extends=columns) % table
        self.run_cmd(cmd)
        return cmd

    def create(self, table, extend_options={}, **kargs):
        """
        this function can create table smarter:
        example:
            create('User', name=str, login_time=time, passwd=hash, own=1, number=int, id_f=Table)
            will ->  CREATE TABLE User (
                            ID INTEGER PRIMARY KEY NOT NULL [AUTO_INCREMENT] ,
                            CreatedTime TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            name TEXT NOT NULL,
                            login_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            passwd text, # hash(str),
                            own INTEGER NOT NULL DEFAULT 1 ,
                            number INTEGER,
                            id_f FOREIGN KEY REFERENCES Table(ID)
            ) 
        """

        columns = {}
        names = []
        for k in kargs:
            names.append(k)
            v = kargs[k]
            if v is int:
                columns[k] = '%s %s' % (k, 'INTEGER ')
            elif v is str:
                columns[k] = '%s %s' % (k, 'TEXT ')
            elif v is time:
                columns[k] = '%s %s' % (k, 'TimeStamp DEFAULT CURRENT_TIMESTAMP')
            elif isinstance(v, int):
                columns[k] = '%s %s' % (k, 'INTEGER NOT NULL DEFAULT %d' % v)
            elif isinstance(v, str):
                columns[k] = '%s %s' % (k, 'VARCHAR(255) NOT NULL DEFAULT "%s"' % v)
            
            elif hasattr(v, '_table'):
                columns[k] = '%s %s' % (k, 'INTEGER, FOREIGN KEY (%s) REFERENCES %s(ID) ' % (k, v.__name__))
            else:
                raise TypeError("not supported Sql Type %s" % str(v))

        # extend some attribute
        for k in extend_options:
            columns[k] += extend_options[k]

        return self.create_table(table, *columns.values())
        

    def drop_table(self, table):
        cmd = 'DROP TABLE %s;' % table
        return self.run_cmd(cmd)

    def close(self):
        try:
            self.cu.close()
            self.con.close()
        except Exception:
            pass
        finally:
            pass

    def __del__(self):
        self.close()

    def _sql(self, k, v):
        if isinstance(v, int):
            return '{}={}'.format(k, v)
        elif isinstance(v, str):
            return '{}="{}"'.format(k, v)
        elif isinstance(v, datetime.datetime):
            return '{}="{}"'.format(k, v)
        elif hasattr(v, '_table'):
            if hasattr(v, "ID"):
                return str(v.ID)
            return 'NULL'
        else:
            print(k, v)
            raise Exception("what type?")

    def select(self,table, *fields, **condition):
        

        cmd = "select {} from %s ".format(",".join(fields)) % table 
        if condition:
            cmd += 'where ' +  ' '.join([self._sql(*i) for i in condition.items()]) + ';'
        # print(cmd)
        self.cu.execute(cmd)
        for row in self.cu.fetchall():
            yield row

    def _sqls(self, i):
        if isinstance(i, int):
            return str(i)
        elif isinstance(i, str):
            return i
        elif hasattr(i, '_table'):
            if hasattr(i, "ID"):
                return str(i.ID)
            return 'NULL'
        elif i is time:
            return datetime.datetime.now()
        elif isinstance(i, datetime.datetime):
            return i
        else:
            print(i)
            raise("error insert")

    def insert(self, table, insert_columns, *values, **kargs):
        values = [ self._sqls(i) for i in values ]
        sept = '?' if self.Type == 'sqlite' else '%s'
        # sept = '%s'
        values_tmp = ','.join([sept for i in range(len(values))])
        cmd = ("insert into %s ({order}) values ({values});" % table).format(order=','.join(insert_columns), values=values_tmp) 
        # print(cmd, values)
        
        self.run_cmd(cmd, *values)
        

    def update(self, table, sets, **condition):
        sept = '?' if self.Type == 'sqlite' else '%s'

        cond = ' '.join([self._sql(*i) for i in condition.items()])
        updated = ','.join([self._sql(*i) for i in sets.items()])
        cmd = '''UPDATE {table}  SET {updated}
        WHERE {condition} ;
        '''.format(table=table, updated=updated, condition=cond)

        # print(cmd)
        return self.run_cmd(cmd)

    def delete(self, table, **condition):
        cond = ''
        if condition:
            cond = 'WHERE ' + ' '.join([self._sql(*i) for i in condition.items()])
        cmd = '''DELETE FROM {table}
        {condition} ;
        '''.format(table=table, condition=cond)

        return self.run_cmd(cmd)
    # def gen_table(self, *columns):
        # create_cmd = 'create '


class Table:
    """
    this is sql Table trans to class
    need set_handle(objhandle)
    """
    _table = 0
    _obj_handler = None

    def __init__(self, handle=None, **kargs):
        # setattr(self.__class__, '_table', self.__class__.__name__)
        self.ID = None
        self.CreatedTime = None
        self._update = {}

        self._table = self.__class__.__name__
        # for k in self._columns():
        #     if k in kargs:
        #         setattr(self, k, kargs[k])
        #     else:
        #         setattr(self, k, self.__class__.__dict__[k])
        if Table._obj_handler is None:
            if handle:
                Table._obj_handler = handle


        for k in kargs:
            if k in self._columns():
                setattr(self, k, kargs[k])
            elif k in ('ID', 'CreatedTime'):
                setattr(self, k, kargs[k])
            else:
                raise TypeError("table %s no such columns %s " %(self._table, k) )

        # for k in self._obj_columns():
        #     Obj = getattr(self.__class__, k)
        #     v = getattr(self, k)
        #     setattr(self, k, self._obj.find_one(Obj, ID=v))

    def __repr__(self):
        return self.__class__.__name__

    @classmethod
    def _set_handle(cls, handler):
        cls._obj_handler = handler

    @classmethod
    def _columns(cls):
        return [i for i in cls.__dict__ if not i.startswith('__')]

    @classmethod
    def _obj_columns(cls):
        return [i for i in cls._columns() if hasattr(getattr(cls, i), '_table') ]

    def _dict(self):
        return {i:self[i] for i in self.__class__.__dict__ if not i.startswith('__')}

    @classmethod
    def _CREATE_ITEMS(cls):
        return {i:cls.__dict__[i] for i in cls.__dict__ if not i.startswith('__')}

    def __getitem__(self, k):
        v = getattr(self, k)
        if hasattr(getattr(self.__class__, k), '_table'):
            vv = getattr(self.__class__, k)
            return self._obj_handler.find_one(vv, ID=v)
        return v

    def __setitem__(self, k, v):
        self._update[k] = v

    def _save(self):
        if self.ID is None:
            return self._obj_handler.add(self)
        return self._obj_handler.save(self)

    def _delete(self):
        return self._obj_handler.delete(self)

    @staticmethod
    def hash( obj):
        return _hash(obj)

    @classmethod
    def _all(cls):
        return list(cls._obj_handler.find(cls))



class SqlObjectEngine:

    def __init__(self, **connect_option):
        self.sql = SqlEngine(**connect_option)

    def create(self, Obj):
        columns = Obj._CREATE_ITEMS()
        self.sql.create(Obj.__name__, **columns)

    def add(self, Obj_self):
        keys = []
        values = []
        _d = Obj_self._dict()
        for i in _d:
            # jump id and createdTime
            if not _d[i]:
                continue
            keys.append(i)
            values.append(_d[i])

        self.sql.insert(Obj_self.__class__.__name__, keys, *values)

    def _find(self, obj, **condition):
        columns = ['ID','CreatedTime'] +obj._columns()
        selected = ','.join(columns)
        return self.sql.select(obj.__name__, selected, **condition)

    def find_one(self, obj, **condition):
        columns = ['ID','CreatedTime'] +obj._columns()
        for row in self._find(obj, **condition):
            return obj(**dict(zip(columns, row)))
            

    def find(self, obj, **condition):
        columns = ['ID','CreatedTime'] +obj._columns()
        for row in self._find(obj, **condition):
            yield obj(**dict(zip(columns, row)))

    def save(self, obj_self):
        columns = ['ID','CreatedTime'] +obj_self._columns()
        if obj_self.ID != None:
            self.sql.update(obj_self._table, obj_self._update, ID=obj_self.ID)
            obj_self._update = {}

    def delete(self, obj_self):
        self.sql.delete(obj_self._table, ID=obj_self.ID)

    def datetime(self, timeobj):
        if isinstance(timeobj, datetime.datetime):
            return timeobj
        elif isinstance(timeobj, str):
            ss = time.strptime(timeobj, '%Y-%m-%d %H:%M:%S')
            return datetime.datetime.fromtimestamp(time.mktime(ss))


