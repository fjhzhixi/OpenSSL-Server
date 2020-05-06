import pymysql

#还没有登陆的异常
class HasnotSigninException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#没有找到账户或者密码错误
class NoneAccountFoundError(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#找到多个账户满足条件
class MultAccountFoundError(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#该账号不是游戏提供商账号
class NotProviderException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#该账号不是提供该游戏的游戏提供商账号
class NotActulProviderException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#该账号不是玩家账号
class NotPlayerException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#该账号不是平台账号
class NotPlatformException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#该账号是平台账号却不是玩家或游戏提供商账号
class PlatformException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#没有找到该游戏
class NoneGameFoundException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error     

#该游戏已经拥有，不能再次拥有
class HasOwnedGameException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error     

#该游戏还未拥有
class DonotOwnGameException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error  

#没有找到该成就的信息
class NoneGameIncentivesFoundException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error  

#该玩家已经拥有了该成就的信息
class MultGameIncentivesFoundException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error  

#该玩家还没有拥有该成就的信息
class DonotHasThisIncentivesException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error  

#没有找到该宣传
class NoneAnnouncementFoundException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error  

#没有找到该宣传评论
class NoneAnnouncementCommentFoundException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error      

#没有找到该帖子
class NonePostFoundException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error  

#没有找到该楼层
class NonePostCommentFoundException(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error     
        
class Sql():
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "xuqiang", "testpython")
        self.cursor = self.db.cursor()
        self.has_login = False
        self.cur_account_id = -1
        self.cur_account_type = -1
        self.cur_account_name = ""

    def sign_out(self):
        self.has_login = False
        self.cur_account_id = -1
        self.cur_account_type = -1
        self.cur_account_name = ""

    def get_cur_account_name(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        return self.cur_account_name

    def get_cur_account_type(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        return self.cur_account_type

    def get_cur_account_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        return str(self.cur_account_id)  

    #允许用户名重名，因此使用account_id登录
    #account_id, password  均为 str类型
    #返回True为登录成功，否则登陆失败
    def sign_in(self, account_id, password):
        
        sql = "select account_type from account where account_id = %s and account_password = \'%s\'" %(account_id, password)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise NoneAccountFoundError(str(account_id))
        elif len(rows) > 1:
            raise MultAccountFoundError(str(account_id))
        else:
            self.has_login = True
            self.cur_account_id = account_id
            self.cur_account_type = rows[0][0]
            if self.cur_account_type == 0:
                self.cur_account_name = "platform"
            elif self.cur_account_type == 1:
                sql = "select player_name from player where account_id = %s" % (account_id)
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                self.cur_account_name = rows[0][0]
            elif self.cur_account_type == 2: 
                sql = "select provider_name from provider where account_id = %s" % (account_id)
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                self.cur_account_name = rows[0][0]
        return True

    """
    插入部分
    """
    #account_type为int型，user_name和account_password为str型
    #返回值为account_id，str型.
    def sign_up(self, account_type, user_name, account_password):
        sql = """
            insert into account (account_type, account_password, submission_date)
            values
            (%d, \'%s\', NOW())
        """ % (account_type, account_password)
        self.cursor.execute(sql)
        self.db.commit()
        sql = """
            select account_id from account order by account_id desc limit 1
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        account_id = str(rows[0][0])
        if account_type == 1:
            sql = """
                insert into player (account_id, player_name, submission_date)
                values
                (%s, \'%s\', NOW())
                """ % (account_id, user_name)
            self.cursor.execute(sql)
            self.db.commit()
        if account_type == 2:
            sql = """
                insert into provider (account_id, provider_name, submission_date)
                values
                (%s, \'%s\', NOW())
                """ % (account_id, user_name)
            self.cursor.execute(sql)
            self.db.commit()
        return account_id

    #输入参数均为str型
    #返回值为game_id，str型.
    #若当前账户不是provider会抛出异常.
    def upload_game(self, game_name, game_price, game_introduce):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 2:
            raise NotProviderException(str(self.cur_account_id))
        sql = """
            insert into game (game_name, game_price, provider, game_praise_rate, game_introduce, submission_date)
            values
            (\'%s\', %s, %s, 1, \'%s\', NOW())
        """ % (game_name, game_price, self.cur_account_id, game_introduce)
        self.cursor.execute(sql)
        self.db.commit()
        sql = """
            select game_id from game order by game_id desc limit 1
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        game_id = str(rows[0][0])
        return game_id

    #所有输入参数均为str类型
    #输出游戏宣发id，游戏宣发评论区id,为str型
    def upload_game_announcement(self, game_id, title, text, picture):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 2:
            raise NotProviderException(str(self.cur_account_id))
        sql = """
            select provider from game where game_id = %s
        """ % (game_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise NoneGameFoundException(game_id)
        provider = str(rows[0][0])
        if int(provider) != int(self.cur_account_id):
            raise NotActulProviderException(str(self.cur_account_id))
        
        sql = """
            insert into game_announcement (game_id, account_id, announcement_comment_area_id, announcement_title, announcement_text, announcement_picture, submission_date)
            values
            (%s, %s, -3, \'%s\', \'%s\', \'%s\', NOW())
        """ % (game_id, str(self.cur_account_id), title, text, picture)
        self.cursor.execute(sql)
        self.db.commit()
        sql = """
            select game_announcement_id from game_announcement order by game_announcement_id desc limit 1
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        game_announcement_id = str(rows[0][0])
        announcement_comment_area_id = game_announcement_id
        sql = """
            update game_announcement set announcement_comment_area_id = %s, submission_date = NOW() where game_announcement_id = %s
        """ % (announcement_comment_area_id, game_announcement_id)
        self.cursor.execute(sql)
        self.db.commit()
        return game_announcement_id, announcement_comment_area_id

    #输入均为str型
    #输出为当前宣传评论区下一楼层层数,为str型
    def upload_announce_comment(self, announcement_comment_area_id, comment_order, comment_text):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            insert into announcement_comment (announcement_comment_area_id, account_id, comment_order, comment_text, submission_date)
            values
            (%s, %s, %s, \'%s\', NOW())
        """ % (announcement_comment_area_id, str(self.cur_account_id), comment_order, comment_text)
        self.cursor.execute(sql)
        self.db.commit()
        return str(int(comment_order) + 1)

    #前端不需要调用
    def upload_feedback(self, text, ttype):
        sql = """
            insert into feedback (feedback_type, submission_date)
            values
            (%d, NOW())
        """ % (ttype)
        self.cursor.execute(sql)
        self.db.commit()

        sql = """
            select feedback_id from feedback order by feedback_id desc limit 1
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        feedback_id = str(rows[0][0])

        return feedback_id

    #输入text为str型
    #输出反馈的id，为str型
    def upload_player_feedback(self, text):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 1:
            raise NotPlayerException(str(self.cur_account_id))
        feedback_id = self.upload_feedback(text, 1)

        sql = """
            insert into player_feedback (feedback_id, account_id, feedback_text, submission_date)
            values
            (%s, %s, \'%s\', NOW())
        """ % (feedback_id, str(self.cur_account_id), text)
        self.cursor.execute(sql)
        self.db.commit()
        return feedback_id

    #输入text为str型
    #输出反馈的id，为str型
    def upload_provider_feedback(self, text):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 2:
            raise NotProviderException(str(self.cur_account_id))
        feedback_id = self.upload_feedback(text, 2)

        sql = """
            insert into provider_feedback (feedback_id, account_id, feedback_text, submission_date)
            values
            (%s, %s, \'%s\', NOW())
        """ % (feedback_id, str(self.cur_account_id), text)
        self.cursor.execute(sql)
        self.db.commit()
        return feedback_id

    #输入account_id, text为str型,请尽可能保证输入的account_id是存在的某个provider或player
    #输出反馈的id，为str型
    def upload_platform_feedback(self, account_id, text):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 0:
            raise NotPlatformException(str(self.cur_account_id))
        sql = """
            select account_type from account where account_id = %s
        """ % (account_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        account_type = rows[0][0]
        if account_type == 0:
            raise PlatformException(account_id)

        feedback_id = self.upload_feedback(text, 0)

        sql = """
            insert into platform_feedback (feedback_id, account_id, feedback_text, submission_date)
            values
            (%s, %s, \'%s\', NOW())
        """ % (feedback_id, account_id, text)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            sql = """
                delete from feedback where feedback_id = %s
            """ % (feedback_id)
            self.cursor.execute(sql)
            self.db.commit()
            raise NoneAccountFoundError(account_id)
        return feedback_id   

    #输入均为str型
    #输出为帖子的id，str型
    def upload_community_post(self, title, text, picture):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            insert into community_post (account_id, post_title, post_text, post_picture, submission_date)
            values
            (%s, \'%s\', \'%s\', \'%s\', NOW())
        """ % (str(self.cur_account_id), title, text, picture)
        self.cursor.execute(sql)
        self.db.commit()

        sql = """
            select community_post_id from community_post order by community_post_id desc limit 1
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        community_post_id = str(rows[0][0])
        return community_post_id

    #输入均为str型
    #输出为帖子下一楼层层数
    def upload_community_comment(self, community_post_id, community_order, text, picture):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        print("********")
        print(community_post_id)
        print(community_order)
        print("********")
        sql = """
            insert into community_comment (community_post_id, community_order, account_id, comment_text, comment_picture, submission_date)
            values
            (%s, %s, %s, \'%s\', \'%s\', NOW())
        """ % (community_post_id, community_order, str(self.cur_account_id), text, picture)
        self.cursor.execute(sql)
        self.db.commit()

        return str(int(community_order) + 1)

    #输入为str型
    #如果成功输出为True
    def upload_owned_game(self, game_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 1:
            raise NotPlayerException(str(self.cur_account_id))

        sql = """
            select game_id from game where game_id = %s
        """ % (game_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            raise NoneGameFoundException(game_id)

        sql = """
            select game_id from owned_game where game_id = %s and account_id = %d
        """ % (game_id, int(self.cur_account_id))
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) > 0:
            raise HasOwnedGameException(game_id + str(self.cur_account_id))

        sql = """
            insert into owned_game (account_id, game_id, submission_date)
            values
            (%s, %s, NOW())
        """ % (str(self.cur_account_id), game_id)

        

        self.cursor.execute(sql)
        self.db.commit()

        sql = """
            select incentives_id from game_incentives where game_id = %s
        """ % (game_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for each in rows:
            sql = """
                insert into incentives_earned (account_id, incentives_id, has_finished, submission_date)
                values
                (%s, %s, 0, NOW())
            """ % (str(self.cur_account_id), each[0])

        return True

    #输入的incentives_type为int型，其余均为str型
    #输出成就id，为str型
    def upload_game_incentives(self, incentives_type, incentives_name, incentives_condition, game_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 2:
            raise NotPlatformException(str(self.cur_account_id))
        
        sql = """
            select game_id from game where game_id = %s
        """ % (game_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            raise NoneGameFoundException(game_id)

        sql = """
            insert into game_incentives (incentives_type, incentives_name, incentives_condition, game_id, submission_date)
            values
            (%d, \'%s\', \'%s\', %s, NOW())
        """ % (incentives_type, incentives_name, incentives_condition, game_id)

        self.cursor.execute(sql)
        self.db.commit()

        sql = """
            select incentives_id from game_incentives order by incentives_id desc limit 1
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        incentives_id = str(rows[0][0])
        return incentives_id

    #输入的has_finished为int型，其余为str型
    #成功插入则输出True
    def upload_incentives_earned(self, incentives_id, has_finished):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 1:
            raise NotPlayerException(str(self.cur_account_id))

        sql = """
            select incentives_id from game_incentives where incentives_id = %s
        """ % (incentives_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            raise NoneGameIncentivesFoundException(incentives_id)
        sql = """
            select incentives_id from incentives_earned where incentives_id = %s and account_id = %d
        """ % (incentives_id, int(self.cur_account_id))
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) > 0:
            raise MultGameIncentivesFoundException(incentives_id + str(self.cur_account_id))

        sql = """
            insert into incentives_earned (account_id, incentives_id, has_finished, submission_date)
            values
            (%d, %s, %d, NOW())
        """ % (int(self.cur_account_id), incentives_id, has_finished)

        self.cursor.execute(sql)
        self.db.commit()
        return True

    def judge_is_provider(self):
        if self.cur_account_type != 2:
            raise NotProviderException(str(self.cur_account_id))

    def judge_is_exist_game(self, game_id):
        sql = """
            select game_id from game where game_id = %s
        """ % (game_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            raise NoneGameFoundException(game_id)

    def has_this_game(self, game_id):
        sql = """
            select game_id from owned_game where game_id = %s and account_id = %s
        """ % (game_id, str(self.cur_account_id))
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            return False

        return True

    def incentives_exists(self, incentives_id):
        sql = """
            select incentives_id from game_incentives where incentives_id = %s
        """ % (incentives_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            return False

        return True

    def has_this_incentives(self, incentives_id):
        sql = """
            select incentives_id from incentives_earned where incentives_id = %s and account_id = %s
        """ % (incentives_id, str(self.cur_account_id))
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            return False

        return True

    """
    更新部分
    """

    #输入均为str类型
    #成功更新则输出True
    def update_game_price(self, game_id, price):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        try:
            self.judge_is_provider()
            self.judge_is_exist_game(game_id)
        except:
            raise
        sql = """
            update game set game_price = %s, submission_date = NOW() where game_id = %s
        """ % (price, game_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True
    
    #输入均为str类型
    #成功更新则输出True
    def update_game_praise_rate(self, game_id, game_praise_rate):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        try:
            self.judge_is_provider()
            self.judge_is_exist_game(game_id)
        except:
            raise
        sql = """
            update game set game_praise_rate = %s, submission_date = NOW() where game_id = %s
        """ % (game_praise_rate, game_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功更新则输出True
    def update_game_introduce(self, game_id, game_introduce):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        try:
            self.judge_is_provider()
            self.judge_is_exist_game(game_id)
        except:
            raise
        sql = """
            update game set game_introduce = %s, submission_date = NOW() where game_id = %s
        """ % (game_introduce, game_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功更新则输出True
    def update_game_picture(self, game_id, game_picture):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        try:
            self.judge_is_provider()
            self.judge_is_exist_game(game_id)
        except:
            raise
        sql = """
            update game set game_picture = \'%s\', submission_date = NOW() where game_id = %s
        """ % (game_picture, game_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True    

    """
    没有给宣传广告提供修改功能
    """

    """
    没有给宣传广告下的评论区提供修改功能
    """

    """
    对于所有的反馈都没有提供修改功能
    """

    """
    帖子及帖子内部的发言也没有修改功能
    """

    #输入均为str类型
    #成功更新则输出True
    def update_account_name(self, name):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type == 0:
            raise PlatformException(str(self.cur_account_id))
        if self.cur_account_type == 1:
            sql = """
                update player set player_name = %s, submission_date = NOW() where account_id = %d
            """ % (name, int(self.cur_account_id))
            self.cursor.execute(sql)
            self.db.commit()
        if self.cur_account_type == 2:
            sql = """
                update provider set provider_name = %s, submission_date = NOW() where account_id = %d
            """ % (name, int(self.cur_account_id))
            self.cursor.execute(sql)
            self.db.commit()
        self.cur_account_name = name
        return True
    
    #输入均为str类型
    #成功更新则输出True
    def update_account_password(self, password):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type == 0:
            raise PlatformException(str(self.cur_account_id))
        sql = """
            update account set account_password = %s, submission_date = NOW() where account_id = %d
        """ % (password, int(self.cur_account_id))
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功更新则输出True
    def update_account_picture(self, picture):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type == 0:
            raise PlatformException(str(self.cur_account_id))
        sql = """
            update account set account_picture = %s, submission_date = NOW() where account_id = %d
        """ % (picture, int(self.cur_account_id))
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功更新则输出True
    def update_owned_game_time(self, game_id, time):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 1:
            raise NotPlayerException(str(self.cur_account_id))
        
        if self.has_this_game(game_id) == False:
            raise DonotOwnGameException(str(self.cur_account_id) + game_id)

        sql = """
            update owned_game set game_time = %s, submission_date = NOW() where game_id = %s and account_id = %d
        """ % (time, game_id, int(self.cur_account_id))
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功更新则输出True
    def update_owned_game_evaluation(self, game_id, evaluation):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 1:
            raise NotPlayerException(str(self.cur_account_id))
        
        if self.has_this_game(game_id) == False:
            raise DonotOwnGameException(str(self.cur_account_id) + game_id)

        sql = """
            update owned_game set game_evaluation = %s, submission_date = NOW() where game_id = %s and account_id = %d
        """ % (evaluation, game_id, int(self.cur_account_id))
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功更新则输出True
    def update_owned_game_comment(self, game_id, game_comment):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 1:
            raise NotPlayerException(str(self.cur_account_id))
        
        if self.has_this_game(game_id) == False:
            raise DonotOwnGameException(str(self.cur_account_id) + game_id)

        sql = """
            update owned_game set game_comment = \'%s\', submission_date = NOW() where game_id = %s and account_id = %d
        """ % (game_comment, game_id, int(self.cur_account_id))
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功更新则输出True
    def update_game_incentives_name(self, incentives_id, name):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 2:
            raise NotProviderException(incentives_id)
        
        if self.incentives_exists(incentives_id) == False:
            raise NoneGameIncentivesFoundException(str(self.cur_account_id) + incentives_id)

        sql = """
            update game_incentives set incentives_name = %s, submission_date = NOW() where incentives_id = %s
        """ % (name, incentives_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True
    
    #输入均为str类型
    #成功更新则输出True
    def update_game_incentives_condition(self, incentives_id, condition):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 2:
            raise NotProviderException(incentives_id)
        
        if self.incentives_exists(incentives_id) == False:
            raise NoneGameIncentivesFoundException(str(self.cur_account_id) + incentives_id)

        sql = """
            update game_incentives set incentives_condition = %s, submission_date = NOW() where incentives_id = %s
        """ % (condition, incentives_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功更新则输出True
    def update_incentives_earned_has_finished(self, incentives_id, has_finished):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 1:
            raise NotPlayerException(str(self.cur_account_id))
        
        if self.has_this_incentives(incentives_id) == False:
            raise DonotHasThisIncentivesException(str(self.cur_account_id) + incentives_id)

        sql = """
            update incentives_earned set has_finished = %s, submission_date = NOW() where incentives_id = %s and account_id = %d
        """ % (has_finished, incentives_id, int(self.cur_account_id))
        self.cursor.execute(sql)
        self.db.commit()
        return True


    """
    删除部分
    """
    #输入均为str类型
    #成功删除则输出True
    def delete_game_announcement(self, game_announcement_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 0:
            raise NotPlatformException(str(self.cur_account_id))
        sql = """
            select announcement_comment_area_id from game_announcement where game_announcement_id = %s
        """ % (game_announcement_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise NoneAnnouncementFoundException(game_announcement_id)
        announcement_comment_area_id = str(rows[0][0])
        sql = """
            select announcement_comment_area_id, comment_order from announcement_comment where announcement_comment_area_id = %s
        """ % (announcement_comment_area_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for each in rows:
            self.delete_announcement_comment(str(each[0]), str(each[1]))
        sql = """
            delete from game_announcement where game_announcement_id = %s
        """ % (game_announcement_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功删除则输出True
    def delete_announcement_comment(self, announcement_comment_area_id, comment_order):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 0:
            raise NotPlatformException(str(self.cur_account_id))
        sql = """
            select account_id from announcement_comment where announcement_comment_area_id = %s and comment_order = %s
        """ % (announcement_comment_area_id, comment_order)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise NoneAnnouncementCommentFoundException(announcement_comment_area_id + comment_order)
        sql = """
            delete from announcement_comment where announcement_comment_area_id = %s and comment_order = %s
        """ % (announcement_comment_area_id, comment_order)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功删除则输出True
    def delete_community_comment(self, community_post_id, community_order):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 0:
            raise NotPlatformException(str(self.cur_account_id))
        sql = """
            select account_id from community_comment where community_post_id = %s and community_order = %s
        """ % (community_post_id, community_order)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise NonePostCommentFoundException(community_post_id + community_order)
        sql = """
            delete from community_comment where community_post_id = %s and community_order = %s
        """ % (community_post_id, community_order)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #输入均为str类型
    #成功删除则输出True
    def delete_community_post(self, community_post_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        if self.cur_account_type != 0:
            raise NotPlatformException(str(self.cur_account_id))
        sql = """
            select community_post_id from community_post where community_post_id = %s
        """ % (community_post_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise NonePostFoundException(community_post_id)
        sql = """
            select community_post_id, community_order from community_comment where community_post_id = %s
        """ % (community_post_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for each in rows:
            self.delete_community_comment(each[0], each[1])
        sql = """
            delete from community_post where community_post_id = %s
        """ % (community_post_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True

    """
    一般查询部分，函数不会抛出异常，注意检查我的返回值
    """
    #无输入
    #输出为列表，列表中每一项为game_id，类型还没有实验,大概率为int型
    def select_game_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select game_id from game
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为game_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（game_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_game(self, game_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from game where game_id = %s
        """ % (game_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['game_id'] = each[0]
            ans['game_name'] = each[1]
            ans['game_price'] = each[2]
            ans['provider'] = each[3]
            ans['game_praise_rate'] = each[4]
            ans['game_introduce'] = each[5]
            ans['game_picture'] = each[6]
            ans['submission_date'] = each[7]
        return ans

    def select_provider_game(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        try:
            self.judge_is_provider()
        except:
            raise
        sql = """
            select game_id, game_name from game where provider = %s
        """ % (self.cur_account_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        print("*************")
        ansans = []
        
        for each in rows:
            ans = {}
            print(each[0])
            print(each[1])
            ans['game_id'] = each[0]
            ans['game_name'] = each[1]
            ansans.append(ans)
        return ansans
    
    #无输入
    #输出为列表，列表中每一项为game_announcement_id，类型还没有实验,大概率为int型
    def select_game_announcement_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select game_announcement_id from game_announcement
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为game_announcement_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（game_announcement_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_game_announcement(self, game_announcement_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from game_announcement where game_announcement_id = %s
        """ % (game_announcement_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['game_announcement_id'] = each[0]
            ans['game_id'] = each[1]
            ans['account_id'] = each[2]
            ans['announcement_comment_area_id'] = each[3]
            ans['announcement_title'] = each[4]
            ans['announcement_text'] = each[5]
            ans['announcement_picture'] = each[6]
            ans['submission_date'] = each[7]
        return ans

    #无输入
    #输出为列表，列表中每一项为announcement_comment_area_id和comment_order组成的列表，类型还没有实验,大概率均为int型
    def select_announcement_comment_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select announcement_comment_area_id, comment_order from announcement_comment
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为announcement_comment_area_id和comment_order,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_announcement_comment(self, announcement_comment_area_id, comment_order):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from announcement_comment where announcement_comment_area_id = %s and comment_order = %s
        """ % (announcement_comment_area_id, comment_order)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['announcement_comment_area_id'] = each[0]
            ans['account_id'] = each[1]
            ans['comment_order'] = each[2]
            ans['comment_text'] = each[3]
            ans['submission_date'] = each[4]
        return ans

    #无输入
    #输出为列表，列表中每一项为account_id，类型还没有实验,大概率为int型
    def select_provider_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select account_id from provider
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为account_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（account_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_provider(self, account_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from provider where account_id = %s
        """ % (account_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['account_id'] = each[0]
            ans['provider_name'] = each[1]
            ans['submission_date'] = each[2]
        return ans

    #无输入
    #输出为列表，列表中每一项为feedback_id，类型还没有实验,大概率为int型
    def select_player_feedback_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select feedback_id from player_feedback
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为feedback_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（feedback_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_player_feedback(self, feedback_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from player_feedback where feedback_id = %s
        """ % (feedback_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['feedback_id'] = each[0]
            ans['account_id'] = each[1]
            ans['feedback_text'] = each[2]
            ans['submission_date'] = each[3]
        return ans

    #无输入
    #输出为列表，列表中每一项为feedback_id，类型还没有实验,大概率为int型
    def select_provider_feedback_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select feedback_id from provider_feedback
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为feedback_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（feedback_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_provider_feedback(self, feedback_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from provider_feedback where feedback_id = %s
        """ % (feedback_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['feedback_id'] = each[0]
            ans['account_id'] = each[1]
            ans['feedback_text'] = each[2]
            ans['submission_date'] = each[3]
        return ans

    #无输入
    #输出为列表，列表中每一项为feedback_id，类型还没有实验,大概率为int型
    def select_platform_feedback_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select feedback_id from platform_feedback
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为feedback_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（feedback_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_platform_feedback(self, feedback_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from platform_feedback where feedback_id = %s
        """ % (feedback_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['feedback_id'] = each[0]
            ans['account_id'] = each[1]
            ans['feedback_text'] = each[2]
            ans['submission_date'] = each[3]
        return ans

    #无输入
    #输出为列表，列表中每一项为feedback_id，类型还没有实验,大概率为int型
    def select_feedback_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select feedback_id from feedback
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为feedback_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（feedback_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_feedback(self, feedback_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from feedback where feedback_id = %s
        """ % (feedback_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['feedback_id'] = each[0]
            ans['feedback_type'] = each[1]
            ans['submission_date'] = each[2]
        return ans

    #无输入
    #输出为列表，列表中每一项为community_post_id，类型还没有实验,大概率为int型
    def select_community_post_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select community_post_id from community_post
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为community_post_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（community_post_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_community_post(self, community_post_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from community_post where community_post_id = %s
        """ % (community_post_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['community_post_id'] = each[0]
            ans['account_id'] = each[1]
            ans['post_title'] = each[2]
            ans['post_text'] = each[3]
            ans['post_picture'] = each[4]
            ans['submission_date'] = each[5]
        return ans

    #无输入
    #输出为列表，列表中每一项为community_post_id与community_order构成的列表，类型还没有实验,大概率均为int型
    def select_community_comment_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select community_post_id, community_order from community_comment
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为community_post_id与community_order,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_community_comment(self, community_post_id, community_order):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from community_comment where community_post_id = %s and community_order = %s
        """ % (community_post_id, community_order)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['community_post_id'] = each[0]
            ans['community_order'] = each[1]
            ans['account_id'] = each[2]
            ans['comment_text'] = each[3]
            ans['comment_picture'] = each[4]
            ans['submission_date'] = each[5]
        return ans

    #无输入
    #输出为列表，列表中每一项为account_id，类型还没有实验,大概率为int型
    def select_player_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select account_id from player
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为account_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（account_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_player(self, account_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from player where account_id = %s
        """ % (account_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['account_id'] = each[0]
            ans['player_name'] = each[1]
            ans['submission_date'] = each[2]
        return ans

    #无输入
    #输出为列表，列表中每一项为account_id，类型还没有实验,大概率为int型
    def select_account_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select account_id from account
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为account_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（account_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_account(self, account_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from account where account_id = %s
        """ % (account_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['account_id'] = each[0]
            ans['account_type'] = each[1]
            ans['account_password'] = each[2]
            ans['account_picture'] = each[3]
            ans['submission_date'] = each[4]
        return ans

    #无输入
    #输出为列表，列表中每一项为account_id与game_id构成的列表，类型还没有实验,大概率均为int型
    def select_owned_game_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select account_id, game_id from owned_game
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为account_id与game_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_owned_game(self, account_id, game_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from owned_game where account_id = %s and game_id = %s
        """ % (account_id, game_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['account_id'] = each[0]
            ans['game_id'] = each[1]
            ans['game_time'] = each[2]
            ans['game_evaluation'] = each[3]
            ans['game_comment'] = each[4]
            ans['submission_date'] = each[5]
        return ans

    #无输入
    #输出为列表，列表中每一项为incentives_id，类型还没有实验,大概率为int型
    def select_incentives_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select incentives_id from game_incentives
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为incentives_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（incentives_id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_game_incentives(self, incentives_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from game_incentives where incentives_id = %s
        """ % (incentives_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['incentives_id'] = each[0]
            ans['incentives_type'] = each[1]
            ans['incentives_name'] = each[2]
            ans['incentives_condition'] = each[3]
            ans['game_id'] = each[4]
            ans['submission_date'] = each[5]
        return ans

    #无输入
    #输出为列表，列表中每一项为account_id与incentives_id构成的列表，类型还没有实验,大概率均为int型
    def select_incentives_earned_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select account_id, incentives_id from incentives_earned
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    #输入为account_id与incentives_id,str型
    #输出为字典，key为表的每一行的名字,这个函数不会抛出异常，请注意判断字典是否为空（id不存在）
    #输出类型还没有检验，大概率等于它在数据库中的存储类型，请注意
    def select_incentives_earned(self, account_id, incentives_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from incentives_earned where account_id = %s and incentives_id = %s
        """ % (account_id, incentives_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        ans = {}
        for each in rows:
            ans['account_id'] = each[0]
            ans['incentives_id'] = each[1]
            ans['has_finished'] = each[2]
            ans['submission_date'] = each[3]
        return ans




    
