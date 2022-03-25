# -*- coding: utf-8 -*-
"""
@Date    : 2022/3/24 17:22
@Author  : Jason Xiong
@FileName: gitlab_group.py
@Describe: 
"""
import gitlab
from util import findGroup


class GitLabGroup:
    def __init__(self, _gitlab):
        self._gitlab = _gitlab
        self.groupObject = None

    def createOrUpdateGroup(self, name, parent, options):
        """

        :param name: group name
        :param parent:  parent name
        :param options:
        :return:
        """
        parent_id = None
        if parent:
            parent_group = self.findParentGroup(parent)
            if parent_group:
                parent_id = self.getGroupId(parent_group)
            else:
                raise Exception("parent don't exists")

        if not self.existsGroup(name):
            # create new group
            self._gitlab.groups.create({
                "name": name,
                "path": options["path"],
                "description": options["description"],
                "parent_id": parent_id,
            })
        else:
            group = self.updateGroup(self.groupObject, {
                "description": options["description"],
                "parent_id": parent_id,
            })
            group.save()

    def deleteGroup(self, name):
        if self.existsGroup(name):
            self.groupObject.delete()

    @staticmethod
    def updateGroup(group, args):
        for key, value in args.items():
            if getattr(group, key) != args[key]:
                setattr(group, key, args[key])

        return group

    def existsGroup(self, name):
        group = findGroup(self._gitlab, name)
        if group:
            self.groupObject = group
            return True
        return False

    def existsParentGroup(self, name):
        group = findGroup(self._gitlab, name)
        return True if group else False

    def findParentGroup(self, name):
        return findGroup(self._gitlab, name)

    @staticmethod
    def getGroupId(group):
        if group is not None:
            return group.id
        return None

    def findGroup(self, name):
        groups = self._gitlab.groups.list(seach=name)

        for group in groups:
            if group.name == name:
                return group

        return


if __name__ == '__main__':
    arguments = dict(
        url="http://192.168.10.30:81/",
        http_username="root",
        http_password="root123456",
        private_token="_s-uwMHQu9ZDSSRyMbyA",
    )

    gitlab_instance = gitlab.Gitlab(**arguments)
    gitlab_instance.auth()

    gitlab_group = GitLabGroup(gitlab_instance)

    # group_args = dict(
    #     path="log_service",
    #     description="......",
    # )
    # gitlab_group.createOrUpdateGroup("log_service", "develop", group_args)

    # group_args = dict(
    #     path="order_service",
    #     description="order service",
    # )
    # gitlab_group.createOrUpdateGroup("order_service", None, group_args)

    gitlab_group.deleteGroup("develop")
