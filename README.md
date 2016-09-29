#Mroylib

> there many parts in Mroylib... 


*all parts*

> ls qlib  
  
 	c.py               io                 searcher           	text
	__init__.py        data               log                	shodan.py          viewer
	file               net                spide              	zoomeye.py
	asyn               graphy             science            	structure

but i just say 'data' and 'asyn'

### data

#### example
	
	
	In [20]: from qlib.data.sql import SqlEngine
	
	In [21]: sql = SqlEngine(database="test", user='root', type='mysql')
	In [22]: sql2 = SqlEngine(database="msf", user='msf', type='postgresql')
	In [23]: sql3 = SqlEngine(database="/tmp/abc.sql") # default sqlite
	
	In [24]: # show time
	
	In [25]: sql.table_list()
	Out[25]: (('ok',),)
	
	In [26]: sql2.table_list()
	Out[26]: (('test',),)
	
	In [27]: sql3.table_list()
	Out[27]: (('abcd',),)
	
	In [28]: # table schema 
	
	In [29]: sql.check_table("ok")
	Out[29]: 
	(('ID', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
	 ('CreatedTime', 'timestamp', 'NO', '', 'CURRENT_TIMESTAMP', ''),
	 ('name', 'varchar(255)', 'NO', '', '1232', ''))
	
	In [30]: sql2.check_table("test")
	Out[30]: 
	(('id', 'integer', "nextval('test_id_seq'::regclass)"),
	 ('createdtime', 'timestamp without time zone', 'now()'),
	 ('i2', 'character varying', "'hello'::character varying"))

	In [31]: sql3.check_table("abcd")
	Out[31]: (('id', 'int'), ('c', 'varchar(20)'), ('ss', 'int', 'default', 'Null'))
	
	In [32]: # create new table
	
	In [33]: import time
	
	In [34]: sql.create('table_1', name='name', passwd='pass', content=str, ftime=time)
	Out[34]: "CREATE TABLE table_1 (\n        ID INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT ,\n        CreatedTime TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \n        ftime TimeStamp DEFAULT CURRENT_TIMESTAMP,\n\tpasswd VARCHAR(255) NOT NULL DEFAULT 'pass',\n\tname VARCHAR(255) NOT NULL DEFAULT 'name',\n\tcontent TEXT );"
	
	In [35]: sql2.create('table_2', name='name', id_2=int, id3=3,content=str, ftime=time)
	Out[35]: "CREATE TABLE table_2 (\n        ID SERIAL PRIMARY KEY ,\n        CreatedTime TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \n        ftime TimeStamp DEFAULT CURRENT_TIMESTAMP,\n\tid_2 INTEGER,\n\tid3 INTEGER NOT NULL DEFAULT 3,\n\tname VARCHAR(255) NOT NULL DEFAULT 'name',\n\tcontent TEXT );"
	
	In [36]: sql3.create('table_3', name='name', passwd='pass', content=str, id_2=2)
	Out[36]: "CREATE TABLE table_3 (\n        ID INTEGER PRIMARY KEY NOT NULL  ,\n        CreatedTime TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \n        id_2 INTEGER NOT NULL DEFAULT 2,\n\tpasswd VARCHAR(255) NOT NULL DEFAULT 'pass',\n\tname VARCHAR(255) NOT NULL DEFAULT 'name',\n\tcontent TEXT );"
	
	In [37]: # insert data
	
	In [38]: sql.insert('table_1', ['name', 'content'], 'shit', 'this is content ........' )
	
	In [39]: sql2.insert('table_2', ['content'], 'i just want to insert content ..' )
	
	In [40]: sql3.insert('table_3', ['content', 'id_2'] , 'postgresql content' , 12323)
	
	 
	


> open a new ipython terminal


	In [1]: from qlib.data.sql import SqlEngine
	
	In [2]: sql = SqlEngine(database="test", user='root', type='mysql')
	
	In [3]: sql2 = SqlEngine(database="msf", user='msf', type='postgresql')
	
	In [4]: sql3 = SqlEngine(database="/tmp/abc.sql") # default sqlite
	
	In [5]: # check table schema
	
	In [6]: sql.check_table('table_1')
	Out[6]: 
	(('ID', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
	 ('CreatedTime', 'timestamp', 'NO', '', 'CURRENT_TIMESTAMP', ''),
	 ('ftime', 'timestamp', 'NO', '', 'CURRENT_TIMESTAMP', ''),
	 ('passwd', 'varchar(255)', 'NO', '', 'pass', ''),
	 ('name', 'varchar(255)', 'NO', '', 'name', ''),
	 ('content', 'text', 'YES', '', None, ''))
	
	In [7]: sql2.check_table('table_2')
	Out[7]: 
	(('id', 'integer', "nextval('table_2_id_seq'::regclass)"),
	 ('createdtime', 'timestamp without time zone', 'now()'),
	 ('ftime', 'timestamp without time zone', 'now()'),
	 ('id_2', 'integer', None),
	 ('id3', 'integer', '3'),
	 ('name', 'character varying', "'name'::character varying"),
	 ('content', 'text', None))
	
	In [8]: sql3.check_table('table_3')
	Out[8]: 
	(('ID', 'INTEGER', 'PRIMARY', 'KEY', 'NOT', 'NULL'),
	 ('CreatedTime', 'TimeStamp', 'NOT', 'NULL', 'DEFAULT', 'CURRENT_TIMESTAMP'),
	 ('id_2', 'INTEGER', 'NOT', 'NULL', 'DEFAULT', '2'),
	 ('passwd', 'VARCHAR(255)', 'NOT', 'NULL', 'DEFAULT', "'pass'"),
	 ('name', 'VARCHAR(255)', 'NOT', 'NULL', 'DEFAULT', "'name'"),
	 ('content', 'TEXT'))
	
	In [9]: # query data
	
	In [10]: # can use first, last, select
	
	In [11]: sql.first("table_1") # sql.first(table, *selct_columns, **kargs) # select function is same
	Out[11]: 
	(1,
	 datetime.datetime(2016, 9, 30, 0, 46, 54),
	 datetime.datetime(2016, 9, 30, 0, 46, 54),
	 'pass',
	 'shit',
	 'this is content ........')
	
	In [12]: # update and delete is same 
	
	In [13]: # show the alter
	
	In [14]: sql.alter("table_1", content=None, new_column='hello', new_column_2=244, ftime=None)
	Out[14]: True
	
	In [15]: sql.check_table('table_1')
	Out[15]: 
	(('ID', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
	 ('CreatedTime', 'timestamp', 'NO', '', 'CURRENT_TIMESTAMP', ''),
	 ('passwd', 'varchar(255)', 'NO', '', 'pass', ''),
	 ('name', 'varchar(255)', 'NO', '', 'name', ''),
	 ('new_column', 'varchar(255)', 'NO', '', 'hello', ''),
	 ('new_column_2', 'int(11)', 'NO', '', '244', ''))
	
	In [16]: 


### asyn
#### example
	In [2]: from qlib.asyn import Exe
	
	In [3]: e = Exe(10)
	
	In [4]: import time
	
	In [5]: def func():
	   ...:     print("start", time.asctime())
	   ...:     time.sleep(2)
	   ...:     print("end", time.asctime())
	   ...:     
	
	In [6]: e.submit(func)
	start Fri Sep 30 01:09:11 2016
	
	In [7]: end Fri Sep 30 01:09:13 2016
	In [7]: 
	
	In [7]: e.timmer(5, func)
	
	In [8]: time.asctime()
	Out[8]: 'Fri Sep 30 01:09:30 2016'
	
	In [9]: start Fri Sep 30 01:09:32 2016
	end Fri Sep 30 01:09:34 2016
	In [9]: 
	
	In [9]: e.map??
	Signature: e.map(func, args_iterable)
	Source:   
	    def map(self, func, args_iterable):
	        for res in self.exe.map(func, args_iterable):
	            yield res
	File:      ~/Documents/code/Python/Mroylib/qlib/asyn/__exp.py
	Type:      method
	
	In [10]: def func(i):
	    ...:     print(i, time.asctime())
	    ...:     time.sleep(2)
	    ...:     print(i,"end", time.asctime())
	    ...:     
	    ...:     
	
	In [11]: e.map(func, range(10))
	Out[11]: <generator object map at 0x1079a82d0>
	
	In [12]: list(e.map(func, range(10)))
	0 Fri Sep 30 01:11:04 2016
	1 Fri Sep 30 01:11:04 2016
	2 Fri Sep 30 01:11:04 2016
	3 Fri Sep 30 01:11:04 2016
	4 Fri Sep 30 01:11:04 2016
	5 Fri Sep 30 01:11:04 2016
	6 Fri Sep 30 01:11:04 2016
	7 Fri Sep 30 01:11:04 2016
	8 Fri Sep 30 01:11:04 2016
	9 Fri Sep 30 01:11:04 2016
	3 end Fri Sep 30 01:11:06 2016
	2 end Fri Sep 30 01:11:06 2016
	5 end Fri Sep 30 01:11:06 2016
	6 end Fri Sep 30 01:11:06 2016
	9 end Fri Sep 30 01:11:06 2016
	1 end Fri Sep 30 01:11:06 2016
	7 end Fri Sep 30 01:11:06 2016
	0 end Fri Sep 30 01:11:06 2016
	8 end Fri Sep 30 01:11:06 2016
	4 end Fri Sep 30 01:11:06 2016
	Out[12]: [None, None, None, None, None, None, None, None, None, None]
	
	In [25]: def func(i):
    ...:     print(i, time.asctime())
    ...:     time.sleep(2)
    ...:     print(i,"end", time.asctime())
    ...:     return (i,)
    ...:     
    ...:     
    ...: 
	
	In [26]: def back(i):
    ...:     print("i got :",i)
    ...:     
    ...:     
	
	In [27]: e.done(func, back, 'as')
		as Fri Sep 30 01:17:15 2016
	
	In [28]: as end Fri Sep 30 01:17:17 2016
		i got : as
	
	In [28]: 




