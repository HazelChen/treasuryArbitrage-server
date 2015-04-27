__author__ = 'luck-mac'
import json
import sys
sys.path.append("..")
import sae.const
import MySQLdb

class user:
    username = ""
    password = ""
    def parse(self):
        ret = {"password":self.password,"username":self.username}
        return json.dumps(ret)
    def add(self):
        db = MySQLdb.connect( user = sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('''select * from USER where uid = '%s' ''' % self.username)
        if cursor.rowcount == 0 :
            cursor.execute('insert into USER values ( %s ,%s) ', [self.username, self.password] )
        else :
            self.username = ''
        db.close()

    def update(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('update USER set password = %s where uid = %s ', [ self.password,self.username] )
        db.close()

    def check(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        # db = MySQLdb.connect(user= 'root' , db= 'njuhq', passwd='' , host='localhost' , port = 3306)
        cursor = db.cursor()
        cursor.execute('select * from USER where uid = %s and password = %s' , [self.username,self.password])
        return cursor.rowcount
        db.close()


class ret:
    result = 1;
    def parse(self):
        ret = {"result":self.result}
        return json.dumps(ret)

class arbitrage:
    id = ""
    name = ""
    value = 0.0
    def toDic(self):
        ret = {"id":self.id,"orientation":self.name,"value":self.value}
        return ret


class record:
    uid = ""
    more_contract = ''
    more_price = 0.0
    blank_contract = ''
    blank_price = 0.0
    time = 0
    bond = 0.0
    hand = 0
    state = 0
    id = 0
    def toDic(self):
        ret ={ "more_contract":self.more_contract, "more_price": self.more_price,
                "blank_contract": self.blank_contract , "blank_price":self.blank_price,
                "time" : self.time , "bond" : self.bond,
                "hand":self.hand,"state":self.state,"id":self.id}
        return ret

    def add(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        my_array  = [self.uid,self.more_contract,self.more_price,self.blank_contract,self.blank_price,self.time,self.bond,self.hand,self.state,self.id]
        cursor.execute('insert into History values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',my_array)
        db.close()
    
    def get(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('select * from History where uid = %s',[self.uid])
        results = cursor.fetchall()

        record_list = []

        for row in results:
            each_record = record()
            each_record.uid = row[0]
            each_record.more_contract = row[1]
            each_record.more_price = row[2]
            each_record.blank_contract = row[3]
            each_record.blank_price = row[4]
            each_record.time = row[5]
            each_record.bond = row[6]
            each_record.hand = row[7]
            each_record.state = row[8]
            each_record.id = row[9]
            record_list.append(each_record.toDic())

        db.close()
        return record_list

    def cancel(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        my_array  = [self.uid,self.more_contract,self.more_price,self.blank_contract,self.blank_price,self.time,self.bond,self.hand,self.state]
        cursor.execute('update History set state = 2 where id = %d' % self.id)
        db.close()

    #done undone cancel over


class repertory:
    uid = ""
    more_contract = ""
    blank_contract = ""
    more_price = 0.0
    blank_price = 0.0
    time = 0
    bond = 0.0
    hand = 0
    id = 0
    def toDic(self):
        return {"uid":self.uid,"more_contract":self.more_contract,"blank_contract":self.blank_contract,"time":self.time,"bond":self.bond,"hand":self.hand,"id":self.id,"blank_price":self.blank_price,"more_price":self.more_price}
    def add (self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('insert into Repertory values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[self.uid,self.more_contract,self.blank_contract,self.more_price,self.blank_price,self.time,self.bond,self.hand,self.id])
        db.close()


    def sell(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('select * from Repertory where ID = %s',[self.id])
        results = cursor.fetchall()
        for row in results:
            self.uid = row[0]
            self.more_contract = row[1]
            self.blank_contract = row[2]
            self.more_price = row[3]
            self.blank_price = row[4]
            self.time = row[5]
            self.bond = row[6]
            self.hand = row[7]
        cursor.execute('delete from Repertory where id = %s',[self.id])
        db.close()


    def get(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('select * from Repertory where uid = %s',[self.uid])
        results = cursor.fetchall()
        repertory_list = []
        for row in results:
            each_repertory = repertory()
            each_repertory.uid = row[0]
            each_repertory.more_contract = row[1]
            each_repertory.blank_contract = row[2]
            each_repertory.more_price = row[3]
            each_repertory.blank_price = row[4]
            each_repertory.time = row[5]
            each_repertory.bond = row[6]
            each_repertory.hand = row[7]
            each_repertory.id = row[8]
            repertory_list.append(each_repertory.toDic())

        db.close()
        return repertory_list

class news:
    time = 0
    source = ''
    content = ''
    title = ''
    def toDic(self):
        return {"source":self.source, "time":self.time, "content":self.content, "title":self.title}


    def get(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT, charset = 'utf8')
        cursor = db.cursor()
        cursor.execute('select * from news')
        results = cursor.fetchall()
        news_list = []
        for row in results:
            new = news()
            new.title = row[0]
            new.source = row[1]
            new.time = row[2]
            new.content = row[3]
            news_list.append(new.toDic())
        db.close()
        return news_list


class finance:
    uid = ""
    time = 0
    total = 0
    invest=0
    free=0
    id = 0
    def toDic(self):
        return {"uid":self.uid, "time":self.time, "total_fund":self.total, "invest_fund":self.invest, "free_fund":self.free,"id":self.id}

    def add(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('insert into Funds values ( %s,%s,%s,%s,%s ,%s)',[self.uid,self.time,self.total,self.invest,self.free,self.id])
        db.close()

    def get(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('select * from Funds where uid = %s',[self.uid])
        results = cursor.fetchall()
        finance_list = []
        for row in results:
            each_finance = finance()
            each_finance.uid = row[0]
            each_finance.time = row[1]
            each_finance.total = row[2]
            each_finance.invest = row[3]
            each_finance.free = row[4]
            each_finance.id = row[5]
            finance_list.append(each_finance.toDic())
        db.close()
        return finance_list

    def getlast(self):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()

        cursor.execute('SELECT * FROM Funds WHERE uid = %s and time >= ALL(SELECT time from Funds where uid = %s)',[self.uid,self.uid])
        finance_list = []
        results = cursor.fetchall()
        for row in results:
            each_finance = finance()
            each_finance.uid = row[0]
            each_finance.time = row[1]
            each_finance.total = row[2]
            each_finance.invest = row[3]
            each_finance.free = row[4]
            each_finance.id = row[5]
            finance_list.append(each_finance)
        db.close()
        return finance_list