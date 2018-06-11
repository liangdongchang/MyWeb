

# 操作数据库工具包

import os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MySites.settings")
django.setup()

from SitesApp.models import *
# 操作表父类，进行增删改查
class OperateTable():

    def __init__(self, obj):
        self.table = obj()
        self.obj = obj

    # 保存
    def saveTable(self,table):
        try:
            table.save()
            return True
        except BaseException as e:
            print(e)
            return False

    # 增加
    def add(self, **kwargs):
        self.table = self.obj()
        for k, v in kwargs.items():
            if hasattr(self.table, k):  # 检查实例是否有这个属性
                print('***z增加***', k, v)
                setattr(self.table, k, v)  # 设置属性值
        return self.saveTable(self.table)

    # 删除
    def delete(self,id):
        self.table = self.query(pk=id).first()
        if self.table:
            setattr(self.table, 'isDelete', True)  # 设置属性值
            return self.saveTable(self.table)
        return False

    # 修改
    def modify(self, id, **kwargs):
        # 查询记录表中第id条记录
        self.table = self.query(pk=id).first()
        if self.table:
            print('修改表记录')
            for k, v in kwargs.items():
                if hasattr(self.table, k) and k != id:  # 检查实例是否有这个属性
                    setattr(self.table, k, v)  # 设置属性值
                    print('***修改***', k, v)
            return self.saveTable(self.table)
        return False

    # 查询
    def query(self, **kwargs):
        return self.obj.objects.filter(**kwargs)


# 继承
# 操作用户表
class OperateUserT(OperateTable):
    def query(self, **kwargs):
        return self.obj.uManager.filter(**kwargs)


# 操作候选者表
class OperateCandidateT(OperateTable):
    def query(self, **kwargs):
        return self.obj.cManager.filter(**kwargs)


# 操作投票类型表
class OperateVoteTypeT(OperateTable):
    def query(self, **kwargs):
        return self.obj.vManager.filter(**kwargs)


# 操作投票记录表
class OperateVoteRecordT(OperateTable):
    pass


# 操作聊天记录表
class OperateChatRecordT(OperateTable):
    def query(self, **kwargs):
        return self.table.crManager.filter(**kwargs)


# 实例化类
# 用户表
opeUserT = OperateUserT(User)
# # 候选者表
opeCandidateT = OperateCandidateT(Candidate)
# # 投票类型表
opeVoteTypeT = OperateVoteTypeT(VoteType)
# 投票记录表
opeVoteRecordT = OperateVoteRecordT(VoteRecord)
# 聊天记录表
opeChatRecordT = OperateChatRecordT(ChatRecord)

if __name__ == '__main__':
    print(opeVoteRecordT.query().first())
    print(opeUserT.query())
    print(User.uManager.get(pk=5))


