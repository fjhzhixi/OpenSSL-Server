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

#账号已存在
class AccountAlreadyExistError(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#文件不存在
class FileNotExistError(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

#存在多个文件
class MultiFilesExistError(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

class Sql():
    def __init__(self, password):
        self.db = pymysql.connect("localhost", "root", password, "netdisk")
        self.cursor = self.db.cursor()
        self.cur_user_id = ''
        self.has_login = False
        self.cur_user_name = ''
    
    def sign_out(self):
        self.has_login = False
        self.cur_user_id = ''
        self.cur_user_name = ''
    
    def get_curent_user_name(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        return self.cur_user_name

    def get_curent_user_id(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        return self.cur_user_id
    
    # 使用user_id和password登录
    # user_id和password为str类型
    # 返回True表示登录成功，否则失败
    def sign_in(self, user_id, password):
        sql = """
            select UserName from User where UserId = \'%s\' and Password = \'%s\'
        """ % (user_id, password)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise NoneAccountFoundError(str(user_id))
        elif len(rows) > 1:
            raise MultAccountFoundError(str(user_id))
        else:
            self.has_login = True
            self.cur_user_id = user_id
            self.cur_user_name = rows[0][0]
        print(self.has_login)
        return True
    
    """
    增
    """
    # user_id, user_name, password都为str类型
    # 返回True表示注册成功，否则失败
    def sign_up(self, user_id, user_name, password):
        sql = "select UserName from User where UserId = \'%s\'" % (user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            raise AccountAlreadyExistError(str(user_id))
        else:
            sql = """
                insert into User (UserId, UserName, Password) values (\'%s\', \'%s\', \'%s\')
            """ % (user_id, user_name, password)
            self.cursor.execute(sql)
            self.db.commit()
            return True
    
    # 参数全为str类型
    # 如果文件存在，则会覆盖原文件
    # 返回True表示上传成功，否则失败
    def upload_file(self, file_name, file_path):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select * from File where FileName = \'%s\' and FilePath = \'%s\' and UserId = \'%s\'
        """ % (file_name, file_path, self.cur_user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            sql = """
                update File set UploadDate = NOW() where FileName = \'%s\' and FilePath = \'%s\' and UserId = \'%s\' 
            """ % (file_name, file_path, self.cur_user_id)
            self.cursor.execute(sql)
            self.db.commit()
        else:
            sql = """
            insert into File (FileName, FilePath, UserId, UploadDate) values (\'%s\', \'%s\', \'%s\', NOW())
            """ % (file_name, file_path, self.cur_user_id)
            self.cursor.execute(sql)
            self.db.commit()
        return True
    
    """
    删
    """
    # 参数全为str类型
    # 返回True表示删除成功，否则失败
    def delete_file(self, file_name, file_path):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select FileId from File where FileName = \'%s\' and FilePath = \'%s\' and UserId = \'%s\'
        """ % (file_name, file_path, self.cur_user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise FileNotExistError(str(file_name))
        elif len(rows) > 1:
            raise MultiFilesExistError(str(file_name))
        else:
            file_id = rows[0][0]
            sql = """
                delete from File where FileId = %s
            """ % (file_id)
            self.cursor.execute(sql)
            self.db.commit()
            return True
    
    """
    改
    """
    # 参数为str类型
    # 返回True表示修改成功
    def change_user_name(self, user_name):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            update User set UserName = \'%s\' 
            where UserId = \'%s\'
        """ % (user_name, self.cur_user_id)
        self.cursor.execute(sql)
        self.db.commit()
        return True
    
    # 参数为str类型
    # 返回True表示修改成功
    def change_file_name(self, new_name, old_name, file_path):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select FileId from File where FileName = \'%s\' and FilePath = \'%s\' and UserId = \'%s\'
        """ % (old_name, file_path, self.cur_user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise FileNotExistError(str(old_name))
        elif len(rows) > 1:
            raise MultiFilesExistError(str(old_name))
        else:
            file_id = rows[0][0]
            sql = """
                update File set FileName = \'%s\'
                where FileId = %s
            """ % (new_name, file_id)
            self.cursor.execute(sql)
            self.db.commit()
            return True
    
    # 参数为str类型
    # 返回True表示修改成功
    def change_file_path(self, new_path, old_path, file_name):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select FileId from File where FileName = \'%s\' and FilePath = \'%s\' and UserId = \'%s\'
        """ % (file_name, old_path, self.cur_user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise FileNotExistError(str(file_name))
        elif len(rows) > 1:
            raise MultiFilesExistError(str(file_name))
        else:
            file_id = rows[0][0]
            sql = """
                update File set FilePath = \'%s\'
                where FileId = %s
            """ % (new_path, file_id)
            self.cursor.execute(sql)
            self.db.commit()
            return True
    
    """
    查
    """
    # 无输入参数
    # 查找当前用户的所有文件id
    # 返回多个元组: ((id1),(id2),...),其中,id类型为int
    def select_all_fileid(self):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select FileId from File
            where UserId = \'%s\'
        """ % (self.cur_user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    # 参数类型为str
    # 根据文件id查找文件名
    # 返回类型为str
    def select_file_name(self, file_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select FileName from File
            where FileId = %s
        """ % (file_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    # 参数类型为str
    # 根据文件id查找文件路径
    # 返回类型为str
    def select_file_path(self, file_id):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select FilePath from File
            where FileId = %s
        """ % (file_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]
    
    # 参数类型为str
    # 根据文件名、文件路径查找文件id
    # 返回类型int
    def select_file_id(self, file_name, file_path):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select FileId from File
            where FileName = \'%s\' and FilePath = \'%s\'
            and UserId = \'%s\'
        """ % (file_name, file_path, self.cur_user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    # 参数类型为str, str
    # 根据用户ID和文件名查找文件路径
    # 返回类型str
    def select_file_path_by_name(self, file_name):
        if self.has_login == False:
            raise HasnotSigninException("has not sign in")
        sql = """
            select FilePath from File
            where UserId = \'%s\' and FileName = \'%s\'
        """ % (self.cur_user_id, file_name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]
    



