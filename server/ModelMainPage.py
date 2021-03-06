import os, sys, time,datetime,copy


from flask_sqlalchemy import SQLAlchemy
from Initialization import Initialization
from Utilities import debug_msg



db = Initialization().get_global_db();

class Users(db.Model):
    __tablename__ = 'Users'
    uid = db.Column(db.Integer,primary_key = True)
    nick_name = db.Column(db.String(64))
    password = db.Column(db.String(64))


    #uid_foreignkey = db.relationship('Second_Category',backref='primary_category')


    @property
    def serialize(self):
        return {
            'uid'                :   self.uid,
            'nick_name'          :   self.nick_name,
            'password'           :   self.password
        }


    @staticmethod
    def generate_fake_data():
            uid = Users.query.count()
            nick_name = "fake_User"
            password = "1234abcd"
            new_user = Users(uid = uid, nick_name=nick_name,password=password)
            db.session.add(new_user)
            db.session.commit()
            return uid

    def __repr__(self):
        return '<Users %r>' % self.id


class Primary_Category(db.Model):
    __tablename__ = 'Primary_Category'
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer)
    name = db.Column(db.String(64))
    color = db.Column(db.String(16))
    logo = db.Column(db.String(1024))
    second_category = db.relationship('Second_Category',backref='primary_category')

    @property
    def serialize(self):
        return {
            'id'                :   self.id,
            'uid'                :   self.uid,
            'name'              :   self.name,
            'color'             :   self.color
        }

    @staticmethod
    def generate_fake_data(uid):
        if uid != None:
            id = Primary_Category.query.count()
            name = "fake_Pri"
            color = "#567"
            logo = "fake.png"
            new_pri = Primary_Category(id = id,uid= uid, name=name,color=color,logo=logo)
            db.session.add(new_pri)
            db.session.commit()
            return id
        else:
            return None

    def __repr__(self):
        return '<Primary_Category %r>' % self.id


class Second_Category(db.Model):
    __tablename__ = 'Second_Category'
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer)
    primary_id = db.Column(db.Integer, db.ForeignKey('Primary_Category.id'))
    name = db.Column(db.String(64))
    color = db.Column(db.String(16))
    logo = db.Column(db.String(1024))
    blocks = db.relationship('Blocks',backref = 'second_category')

    @property
    def serialize(self):
        return {
            'id'                :   self.id,
            'uid'                :   self.uid,
            'primary_id'        :   self.primary_id,
            'name'              :   self.name,
            'color'             :   self.color
        }

    @staticmethod
    def generate_fake_data(uid,primary_id):
        if uid != None:
            id = Second_Category.query.count()
            primary_id = primary_id
            name = "fake_Sec"
            color = "#567"
            logo = "fake.png"
            new_sec = Second_Category(id = id, primary_id = primary_id,uid= uid, name=name,color=color,logo=logo)
            db.session.add(new_sec)
            db.session.commit()
            return id
        else:
            return None
    
    def __repr__(self):
        return '<Second_Category %r>' % self.id

class Date(db.Model):
    __tablename__ = 'Date'
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer)
    date = db.Column(db.Date)
    last_changed_time = db.Column(db.DateTime)
    blocks = db.relationship('Blocks',backref = 'date')

    #http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
    @property
    def serialize(self):
        return {
            'id'                :   self.id,
            'uid'                :   self.uid,
            'date'              :   self.date,
            'last_changed_time' :   self.last_changed_time
        }

    @staticmethod
    def generate_fake_data(uid):
        if uid != None:
            id = Date.query.count()
            date = datetime.date.today()
            last_changed_time = datetime.datetime.now()
            new_sec = Date(id = id, uid= uid, date=date,last_changed_time=last_changed_time)
            db.session.add(new_sec)
            db.session.commit()
            return id
        else:
            return None

    def __repr__(self):
        return '<Date %r>' % self.id


class Blocks(db.Model):
    __tablename__ = 'Blocks'
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer)
    date_id = db.Column(db.Integer,db.ForeignKey('Date.id'))
    display_time = db.Column(db.String(16))
    position = db.Column(db.Integer)
    second_category_id = db.Column(db.Integer,db.ForeignKey('Second_Category.id'))

    @property
    def serialize(self):
        return {
            'id'                :   self.id,
            'uid'                :   self.uid,
            'date_id'           :   self.date_id,
            'display_time'      :   self.display_time,
            'position'          :   self.position,
            'second_category_id':   self.second_category_id
        }

    @staticmethod
    def get_block_from_date_id(self,date_id,uid):
        ret = Blocks.query.filter_by(date_id = date_id,uid=uid).all()
        return ret

    @staticmethod
    def update_a_block(self,id,uid,second_category_id):
        ret = Blocks.query.filter_by(id = id,uid= uid).first()
        if ret == None:
            return None
        else:
            ret.second_category_id = second_category_id
            db.session.add(ret)
            db.session.commit()

    @staticmethod
    def create_empty_blocks(uid,date_id,second_category_id):
        new_block = {}
        new_blocks_start_id = Blocks.query.count()
        for index in range(new_blocks_start_id, new_blocks_start_id+48):
            pos = index - new_blocks_start_id
            display_time = "%02d:%02d" % (pos/2, (pos%2)*30)
            new_block[pos] = Blocks(id = index,date_id =date_id,\
                               display_time = display_time,\
                              position = pos,\
                               second_category_id = second_category_id \
                              )
            db.session.add(new_block[pos])
        db.session.commit()
        return 0

    @staticmethod
    def generate_fake_data(uid,date_id,second_category_id):
        return Blocks.create_empty_blocks(uid,date_id,second_category_id)

    def __repr__(self):
        return '<Blocks %r>' % self.id




class ModelMainPage:
    class __ModelMainPage:
        db = None
        def __init__(self):
            pass
        def initialize_database(self, db):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            self.db = db
            db.create_all();
            debug_msg("Users: %d" % Users.query.count())
            debug_msg("Primary_Category: %d" % Primary_Category.query.count())
            debug_msg("Second_Category: %d" % Second_Category.query.count())
            debug_msg("Date: %d" % Date.query.count())
            debug_msg("Blocks: %d" % Blocks.query.count())
            return 0;
        def generate_fake_data(self):
            uid = Users.generate_fake_data();
            pri_id = Primary_Category.generate_fake_data(uid)
            sec_id = Second_Category.generate_fake_data(uid,pri_id)
            date_id = Date.generate_fake_data(uid)
            Blocks.generate_fake_data(uid,date_id,sec_id)
            return 0;


        def update_last_changed_date(self,date_id):
            if date_id is None:
                return None
            date_obj = Date.query.filter_by(id = date_id).first()
            if date_obj is None:
                return None
            last_changed_time = datetime.datetime.now().replace(microsecond = 0)
            date_obj.last_changed_time = last_changed_time
            self.db.session.add(date_obj)
            debug_msg("committed")
            return 0
        ## 
        # @brief create an empty in database
        # 
        # @param input_date datetime.date object
        # 
        # @returns   
        def create_an_empty_day(self,input_date):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            if not db == None:
                if 0== Date.query.filter_by(date=input_date).count():
                    debug_msg("This is a brand new day!!")

                    last_changed_time = datetime.datetime.now().replace(microsecond = 0)
                    new_date_id = Date.query.count() 
                    new_date = Date(id = new_date_id,\
                                    date = input_date,\
                                   last_changed_time =  last_changed_time\
                                   )
                    self.db.session.add(new_date)
                    debug_msg("new Date id: %d,date: %s,last_changed_time :%s" %
                              (new_date.id,new_date.date,new_date.last_changed_time))
                    self.db.session.commit()
                    debug_msg("committed")

                    new_block={}
                    new_blocks_start_id = Blocks.query.count()
                    for index in range(new_blocks_start_id, new_blocks_start_id+48):
                        pos = index - new_blocks_start_id
                        print pos
                        display_time = "%02d:%02d" % (pos/2, (pos%2)*30)
                        new_block[pos] = Blocks(id = index,date_id =new_date_id,\
                                           display_time = display_time,\
                                          position = pos,\
                                           second_category_id = 0 \
                                          )
                        self.db.session.add(new_block[pos])
                        debug_msg("new Blocks[%d] id: %d,date_id: %s,display_time: %s,pos: %d, second_category_id: %d"%
                              (pos,new_block[pos].id,\
                                new_block[pos].date_id,\
                                new_block[pos].display_time,\
                                new_block[pos].position,\
                                new_block[pos].second_category_id))


                    self.db.session.commit()
                    debug_msg("committed")
                    return 0
                else:
                    debug_msg("this day already existed")
                    return None

        ## 
        # @brief create today
        # 
        # @returns   
        def create_today(self):
            ret = self.create_an_empty_day(datetime.datetime.now().date())
            if ret is  None:
                return None
            else:
                return 0

        ## 
        # @brief get a date_id from a date
        # 
        # @param input_date datetime.date object
        # 
        # @returns  date item
        def get_Date(self,input_date):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            date_info = Date.query.filter_by(date = input_date).first()
            if date_info is None:
                debug_msg("cannot find data of this day: %s!" % input_date)
                return None
            if Date.query.filter_by(date = input_date).count() > 1:
                debug_msg("Date conflict!")
                return None
            debug_msg( "date(%s)==>Date item(id=%s)" %(input_date,date_info.serialize['id']))
            return date_info.serialize

        def get_Blocks_from_date_id(self, date_id):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            blocks_info = Blocks.query.filter_by(date_id = date_id).all()
            if blocks_info is None:
                debug_msg("cannot find data of this date id %d" % date_id)
                return None
            ret = []
            for block in blocks_info:
                ret.append(block.serialize)
            debug_msg("date_id(%s)==>Blocks list(%d)" % (date_id, len(blocks_info)))
            return ret
                    
        def get_Second_Category_from_id(self,id):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            info = Second_Category.query.filter_by(id = id).all()
            if (info == []):
                debug_msg("cannot find Second_Category item of this date id %d" % id)
                return None
            if len(info) > 1:
                debug_msg("Second_Category conflict!")
                return None
            info = info[0]
            debug_msg(info.serialize)
            return info.serialize
        def get_Primary_Category_from_id(self,id):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            info = Primary_Category.query.filter_by(id = id).all()
            if info == []:
                debug_msg("cannot find Primary_Category item of this date id %d" % id)
                return None
            if len(info) > 1:
                debug_msg("Primary_Category conflict!")
                return None
            info = info[0]
            debug_msg(info.serialize)
            return info.serialize
        
        def get_all_Second_Category_from_Primary_id(self,primary_id):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            info = Second_Category.query.filter_by(primary_id = primary_id).all()
            if info is None:
                debug_msg("cannot find Second_Category item of this date id %d" % id)
                return None
            ret = []
            
            for each_category in info:
                ret.append(each_category.serialize)
            debug_msg(ret)
            return ret

        def get_all_Primary_Category(self):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            info = Primary_Category.query.all()
            if info is None:
                debug_msg("cannot find Primary_Category item of this date id %d" % id)
                return None
            ret = []
            for each_category in info:
                ret.append(each_category.serialize)
            debug_msg(ret)
            return ret
        def get_all_Category(self):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            ret = copy.deepcopy(self.get_all_Primary_Category())
            if ret is None:
                return None
            for each_obj in ret:
                each_obj['second_category']=self.get_all_Second_Category_from_Primary_id(each_obj['id'])
            debug_msg(ret)
            return ret





        ## 
        # @brief get full data of a day, (no necessary for primary, reduce the data?)
        # 
        # @param date
        # 
        # @returns dict!
        '''
            Data Structure
            {
            id:0,
            last_changed_time:yyyy-mm-dd HH:mm:ss
            Blocks:{
                    {
                    id:0,
                    data_id:0,
                    display_time      :   00:00,
                    position          :   0,
                    second_category_id:   0,
                    second_category:{
                            id:   0,
                            primary_id:   0,
                            name:   jogging,
                            color:   03ff03,
                                }
                    },
                    {

                    }
                    }

            }
        '''
        def get_block_info_from_date(self,date):
            debug_msg(">>> %s.%s" %( __name__,sys._getframe().f_code.co_name))
            ret={}
            if date is None:
                debug_msg("None value")
                return None
            date_dict = self.get_Date(date)
            if date_dict is None:
                debug_msg("None value")
                return None

            #turn datetime to string
            date_dict['date'] = date_dict['date'].strftime("%Y-%m-%d")
            date_dict['last_changed_time'] = date_dict['last_changed_time'].strftime("%Y-%m-%d %H:%M:%S")

            blocks_list = self.get_Blocks_from_date_id(date_dict['id'])
            for block in blocks_list:
                second_category_dict = self.get_Second_Category_from_id(block['second_category_id'])
                block['second_category'] = second_category_dict

            ret = copy.deepcopy(date_dict)
            ret['Blocks'] = copy.deepcopy(blocks_list)
            return ret

        def add_a_Primary_Category(self,name,color):
            if (name or color )is None:
                return None
            exist = Primary_Category.query.filter_by( name = name).count()
            print exist
            if not (exist == 0):
                new_id = Primary_Category.query.filter_by( name = name).first().serialize['id']
                debug_msg("conflit category existed (id = %d),modify it"% new_id)
            else:
                new_id = Primary_Category.query.count()
            new_Primary_Category = Primary_Category(id = new_id, name=name, color=color)
            self.db.session.add(new_Primary_Category)
            self.db.session.commit()
            debug_msg("committed")
            return 0
            
        def add_a_Second_Category(self,name,color,primary_id):
            if (name or color or primary_id )is None:
                return None
            exist = Second_Category.query.filter_by( name = name).count()
            if not (exist == 0):
                new_id = Second_Category.query.filter_by( name = name,primary_id= primary_id).first().serialize['id']
                debug_msg("conflit category existed (id = %d),modify it"% new_id)
            else:
                new_id = Second_Category.query.count()
            new_Second_Category = Second_Category(id = new_id, name=name, color=color,primary_id=primary_id)
            self.db.session.add(new_Second_Category)
            self.db.session.commit()
            debug_msg("committed")
            return 0
        
        def update_a_block(self, block_info):
            if block_info is None:
                return None
            id = block_info['id']
            
            block_obj = Blocks.query.filter_by(id = id).first()
            
            if block_obj is None:
                return None

            block_obj.second_category_id = block_info['second_category_id']

            self.db.session.add(block_obj)
            self.db.session.commit()
            self.update_last_changed_date(block_info['date_id'])
            debug_msg("committed")
            return 0



            
            


            





                


    #for singleton
    instance = None
    def __init__(self):
        if not ModelMainPage.instance:
            ModelMainPage.instance = ModelMainPage.__ModelMainPage()
            
    def __getattr__(self,name):
        return getattr(self.instance, name)




