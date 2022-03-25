# -*- coding: utf-8 -*-
"""
@Date    : 2022/3/23 15:55
@Author  : Jason Xiong
@FileName: case.py
@Describe:
"""
import gitlab
from util import readFile, findGroup, findMember, addUserToGroup
from const import AccessLevel


class GitLabUser:
    def __init__(self, _gitlab):
        self._gitlab = _gitlab
        self.userObject = None

    def existsUser(self, username):
        """ 用户是否存在 """
        user = self.findUser(username)
        if user:
            self.userObject = user
            return True

        return False

    def findUser(self, username):
        users = self._gitlab.users.list(seach=username)

        for user in users:
            if user.username == username:
                return user

        return

    def CreateOrUpdateUser(self, username, options):
        """ 创建或更新用户 """
        # create new user
        if not self.existsUser(username) or not self.userObject:
            user = self._gitlab.users.create({
                "name": options["name"],
                "username": username,
                "password": options["password"],
                "email": options["email"],
            })

        else:
            # update user
            user = self.updateUser(self.userObject, {
                "name": options["name"],
                "username": username,
                "is_admin": options["is_admin"],
            })

        sshKey_name = options.get("sshkey_name")
        sshKey_file = options.get("sshkey_file")
        if sshKey_name and sshKey_file:
            self.addSshKeyToUser(user, {
                "name": sshKey_name,
                "file": sshKey_file,
            })

        # Assign group
        group_path = options.get("group_path")
        access_level = options.get("access_level")
        if group_path:
            self.assignUserToGroup(user, group_path, access_level)

        user.save()

    def deleteUser(self, username=None):
        """ 删除指定用户 """
        if username:
            self.existsUser(username)

        if self.userObject:
            self.userObject.delete()

    @staticmethod
    def updateUser(user, args):
        for key, value in args.items():
            if getattr(user, key) != args[key]:
                setattr(user, key, args[key])

        return user

    @staticmethod
    def sshKeyExists(user, key_name):
        ssh_keys = user.keys.list()
        for key in ssh_keys:
            if key.title == key_name:
                return True

        return False

    def addSshKeyToUser(self, user, sshkey):
        name = sshkey["name"]
        file = sshkey["file"]
        if not self.sshKeyExists(self.userObject, name):
            try:
                user.keys.create({
                    'title': name,
                    'key': readFile(file),
                })
            except gitlab.GitlabCreateError:
                raise Exception("current ssh_key has created in other accounts")

            return True
        return False

    def assignUserToGroup(self, user, group_identifier, access_level):
        group = findGroup(self._gitlab, group_identifier)

        if group is None:
            return False

        uid = self.getUserId(user)
        if self.memberExists(group, uid):
            member = self.findMember(group, uid)
            if not self.memberAsGoodAccessLevel(group, member.id, access_level):
                member.access_level = access_level
                member.save()
            else:
                addUserToGroup(group, uid, access_level)

    @staticmethod
    def getUserId(user):
        if user is not None:
            return user.id
        return None

    def groupExists(self, group_name):
        groups = self._gitlab.groups.list()
        for g in groups:
            if g.name == group_name:
                return True
        return False

    def memberExists(self, group, user_id):
        member = self.findMember(group, user_id)
        return member is not None

    @staticmethod
    def findMember(group, identifier):
        try:
            member = group.members.get(identifier)
        except Exception as e:
            return None
        return member

    @staticmethod
    def memberAsGoodAccessLevel(group, user_id, access_level):
        number = findMember(group, user_id)
        return number.access_level == access_level


if __name__ == '__main__':
    arguments = dict(
        url="http://192.168.10.30:81/",
        http_username="root",
        http_password="root123456",
        private_token="_s-uwMHQu9ZDSSRyMbyA",
    )

    gitlab_instance = gitlab.Gitlab(**arguments)
    gitlab_instance.auth()

    user_args = dict(
        name="zs",
        password="zhangsan123",
        email="jasonminghao@163.com",
        is_admin=True,
        group_path="develop",
        access_level=AccessLevel.Guest
        # sshkey_name="JasonXiong",
        # sshkey_file="/Users/xiongminghao/.ssh/id_rsa.pub",
    )

    gitlab_user = GitLabUser(gitlab_instance)

    # gitlab_user.deleteUser("zhangsan")
    # user_exists = gitlab_user.existsUser("zhangsan")
    gitlab_user.CreateOrUpdateUser("zhangsan", user_args)
