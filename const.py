# -*- coding: utf-8 -*-
"""
@Date    : 2022/3/24 16:47
@Author  : Jason Xiong
@FileName: const.py
@Describe: 
"""
from gitlab.const import (
    NO_ACCESS,
    MINIMAL_ACCESS,
    GUEST_ACCESS,
    REPORTER_ACCESS,
    DEVELOPER_ACCESS,
    MAINTAINER_ACCESS,
    OWNER_ACCESS,
)


class AccessLevel(object):
    """
    docs：https://docs.gitlab.com/ee/api/members.html
    """

    NO_ACCESS = NO_ACCESS
    Minimal_ACCESS = MINIMAL_ACCESS
    Guest = GUEST_ACCESS
    Reporter = REPORTER_ACCESS
    Developer = DEVELOPER_ACCESS
    Maintainer = MAINTAINER_ACCESS
    Owner = OWNER_ACCESS


class ProjectAccessLevel(object):
    """

    """
    Disabled = "disabled"  # 关闭
    Enabled = "enable"  # 启用
    Private = "private"  # 私有
    Public = "public"  # 公开
