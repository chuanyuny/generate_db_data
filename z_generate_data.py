#-*- coding:utf-8 -*-

import sys
import codecs
import os,sys,pathlib
# sys.path.append(pathlib.Path(__file__).parent.parent.__str__())
sys.path.append("D:\Program Files\CloudForensic\CloudSupport\Bin64")
import pyMyDatabase                 #导入美亚数据库Python模块

# print(dir(pyMyDatabase.SQLiteStatement))
def get_db_table(strdbpath):
    # print(pyMyDatabase.getSQLiteVer())
    # print(pyMyDatabase.getSQLiteVerNum())
    # print(sys.getdefaultencoding())
    bThrdSafe = pyMyDatabase.getSQLiteThreadsafe()
    if bThrdSafe == 1:
        pass
        # print("SQLite is Thread safe in pyMyDatabase!")
    else:
        pass
        # print("SQLite is not Thread safe in pyMyDatabase!")
        
    SQLITE_OPEN_READONLY = 0x00000001   #只读模式打开数据库文件
    SQLITE_OPEN_READWRITE = 0x00000002  #读写模式打开数据库文件
    #第一个参数是数据库路径和名称，第二个参数是数据库是否有密码，第三个参数是打开模式，第四个参数是打开等待时间，第五个参数是journal_mode默认为false，第六个参数是VFS flag默认为None即可
    oDb = pyMyDatabase.SQLiteDatabase(strdbpath, True) #精简参数版

    all_table_name=[]
    #cursor=c.execute("SELECT name FROM sqlite_master WHERE type='table' order by name")
    strSQL="SELECT name FROM sqlite_master WHERE type='table' order by name"
    oSmt = pyMyDatabase.SQLiteStatement(oDb, strSQL) #执行查询语句
    while oSmt.executeStep():
        if oSmt.getColumn(0).getText("")!="sqlite_sequence":
            all_table_name.append(oSmt.getColumn(0).getText(""))
    
    oDb.close() #关闭数据库

    return all_table_name    #list,返回结果为给定数据库的所有表名

def write_to_txt(path,content):
    path='./table_data/'+path+'.txt'
    fw=open(path,'a',encoding="utf-8")
    fw.writelines(content)
    fw.close()

def get_db_data(strdbpath):  #strdbpath为数据库目录及数据库名称
    # print(pyMyDatabase.getSQLiteVer())
    # print(pyMyDatabase.getSQLiteVerNum())
    # print(sys.getdefaultencoding())
    bThrdSafe = pyMyDatabase.getSQLiteThreadsafe()
    if bThrdSafe == 1:
        pass
        # print("SQLite is Thread safe in pyMyDatabase!")
    else:
        pass
        # print("SQLite is not Thread safe in pyMyDatabase!")
        
    SQLITE_OPEN_READONLY = 0x00000001   #只读模式打开数据库文件
    SQLITE_OPEN_READWRITE = 0x00000002  #读写模式打开数据库文件
    #第一个参数是数据库路径和名称，第二个参数是数据库是否有密码，第三个参数是打开模式，第四个参数是打开等待时间，第五个参数是journal_mode默认为false，第六个参数是VFS flag默认为None即可
    oDb = pyMyDatabase.SQLiteDatabase(strdbpath, True) #精简参数版
    if oDb != None:
        if (oDb.isOpen() != True):
            print('Database can not be open.')
            return 0
    
        db_table_name=get_db_table(strdbpath)  #给定数据库的所有表名
        for each in db_table_name:  #each表示一个表名
            try:
                strSQL = 'select * from ' + each
                oSmt = pyMyDatabase.SQLiteStatement(oDb, strSQL) #执行查询语句
                columncount=oSmt.getColumnCount()   #求出表中一共有多少列
                while oSmt.executeStep():
                    each_row=[]
                    for i in range(columncount):
                        each_row.append(oSmt.getColumn(i).getText(""))
                    write_to_txt(each,str(tuple(each_row))+'\n')
            except:
                print("%s表数据生成失败！"%each)
            else:
                #如果数据库中对应表内容为空，那在table_data中不会生成相应的文本文档。
                print("%s表数据生成成功！"%each)

        oDb.close() #关闭数据库
        return 1
    else:
        return 0

if __name__ == '__main__':
    all_db=["AppURLs.amf"]
    for each_db in all_db:
        get_db_data(each_db)
    
