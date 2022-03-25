# -*- coding: utf-8 -*-
"""
@Date    : 2022/3/23 17:20
@Author  : Jason Xiong
@FileName: util.py
@Describe: 
"""
import os


def readFile(path):
    """ read file data """
    if not os.path.exists(path):
        return FileExistsError(f"file path: {path} not exists")

    return open(path).read()


def findGroup(gl, identifier):
    try:
        group = gl.groups.get(identifier)
    except Exception as e:
        return None

    return group


def findMember(group, identifier):
    try:
        member = group.members.get(identifier)
    except Exception as e:
        return None

    return member


def findUser(gl, identifier):
    try:
        user = gl.users.get(identifier)
    except Exception as e:
        return None

    return user


def addUserToGroup(group, user_id, level):
    member = group.members.create({
        'user_id': user_id,
        'access_level': level
    })
    return member
