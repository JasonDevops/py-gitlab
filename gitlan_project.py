# -*- coding: utf-8 -*-
"""
@Date    : 2022/3/25 16:20
@Author  : Jason Xiong
@FileName: gitlan_project.py
@Describe: 
"""
import gitlab
from gitlab_user import GitLabUser
from gitlab_group import GitLabGroup


class GitLabProject:
    def __init__(self, _gitlab):
        self._gitlab = _gitlab
        self.projectObject = None

    def createOrUpdateProject(self, name, options):
        """ Create a project base global
        """
        if not self.existProject(name):
            self.createProject(self._gitlab, name, options)

    def createProjectForUser(self, username, project_name, options):
        """ Create a project for an user（admin only）
        """
        gitlab_user = GitLabUser(self._gitlab)
        user = gitlab_user.findUser(username)
        if user:
            if not self.existProject(project_name):
                self.createProject(user, project_name, options)
            # else:
            #     self.updateProject(self.projectObject, {
            #         "description": options.get("description"),
            #         "requirements_access_level": options.get("requirements_access_level"),
            #     })

    def createProjectForGroup(self, group_name, project_name, option):
        """ Create a project in a group
        """
        gitlab_group = GitLabGroup(self._gitlab)
        group = gitlab_group.findGroup(group_name)
        if group:
            self.createProject(group, project_name, option)

    @staticmethod
    def createProject(gl, name, options):
        try:
            project = gl.projects.create({
                'name': name
            })
        except gitlab.GitlabCreateError:
            raise Exception("project has existed")

        return project

    @staticmethod
    def updateProject(project, args):
        for key, value in args.items():
            if getattr(project, key) != args[key]:
                setattr(project, key, args[key])

        return project

    def assignUserToProject(self, username, project_name, access_level):
        """ Assign a user to project

        :return:
        """
        # user exist
        user = GitLabUser(self._gitlab)
        if not user.existsUser(username):
            return Exception("user not exist...")

        # project exist
        if not self.existProject(project_name):
            return Exception("project not exist...")

        # user exist in project
        member = self.findMember(self.projectObject, username)
        if not member:
            self.projectObject.members.create({
                'user_id': user.userObject.id,
                'access_level': access_level
            })
        else:
            if member.access_level != access_level:
                member.access_level = access_level
                member.save()

    def existProject(self, name):
        project = self.findProject(name)
        if project:
            self.projectObject = project
            return True
        return False

    def deleteProject(self, name):
        if self.existProject(name):
            self.projectObject.delete()

    def deleteMember(self, username, project_name):
        if self.existProject(project_name):
            user = self.findMember(self.projectObject, username)
            if user:
                self.projectObject.members.delete(user.id)

    def findProject(self, name):
        projects = self._gitlab.projects.list(search=name)
        for project in projects:
            if project.name == name:
                return project

    @staticmethod
    def findMember(project, username):
        members = project.members.list(query=username)
        for member in members:
            if member.username == username:
                return member


if __name__ == '__main__':
    arguments = dict(
        url="http://192.168.10.30:81/",
        http_username="root",
        http_password="root123456",
        private_token="_s-uwMHQu9ZDSSRyMbyA",
    )

    gitlab_instance = gitlab.Gitlab(**arguments)
    gitlab_instance.auth()

    gitlab_project = GitLabProject(gitlab_instance)

    project_args = dict(
        description="..."
    )
    # gitlab_project.createOrUpdateProject("fpcx", project_args)
    # gitlab_project.createProjectForUser("zhangsan", "xws", project_args)
    # gitlab_project.createProjectForGroup("order_service", "xws", project_args)
    # gitlab_project.assignUserToProject("zhangsan", "fpcx", AccessLevel.Guest)
    gitlab_project.deleteMember("zhangsan", "fpcx")

    # group_args = dict(
    #     path="order_service",
    #     description="order service",
    # )
    # gitlab_group.createOrUpdateGroup("order_service", None, group_args)

    # gitlab_group.deleteGroup("develop")
