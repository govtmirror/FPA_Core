# -*- coding: utf-8 -*-
"""
    flaskbb.utils.permissions
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    A place for all permission checks

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import abort
from functools import wraps
from flask.ext.login import current_user



def check_perm(user, perm, forum, post_user_id=None):
    """Checks if the `user` has a specified `perm` in the `forum`
    If post_user_id is provided, it will also check if the user
    has created the post

    :param user: The user for whom we should check the permission

    :param perm: The permission. You can find a full list of available
                 permissions here: <INSERT LINK TO DOCS>

    :param forum: The forum where we should check the permission against

    :param post_user_id: If post_user_id is given, it will also perform an
                         check if the user is the owner of this topic or post.
    """
    if is_moderator(user=current_user):
        return True

    #need to check the permissions
    return post_user_id == user.id and not getattr(user, "is_lockdownuser", False)
        # return True
        # #need to figure someting out here
        # return user.permissions[perm] and user.id == post_user_id

    # return not user.permissions['banned'] and user.permissions[perm]


def is_authenticated(user = False):
    if user:
        return user.is_authenticated and getattr(user, 'verified', False) and not getattr(user, "is_lockdownuser", False)
    else:
        return current_user.is_authenticated and getattr(current_user, 'verified', False) and not getattr(current_user, "is_lockdownuser", False)

def is_moderator(user = False):
    """Returns ``True`` if the user is in a moderator or super moderator group.

    :param user: The user who should be checked.
    """
    if user:
        return getattr(user, "moderator", False) or getattr(user, "admin", False)
    else:
        return getattr(current_user, "moderator", False) or getattr(current_user, "admin", False)


def is_admin(user = False):
    """Returns ``True`` if the user is a administrator.

    :param user:  The user who should be checked.
    """
    if user:
        return getattr(user, "admin", False)
    else:
        return getattr(current_user, "admin", False)


def is_admin_or_moderator(user=False):
    """Returns ``True`` if the user is either a admin or in a moderator group

    :param user: The user who should be checked.
    """
    if user:
        return getattr(user, "moderator", False) or getattr(user, "admin", False)
    else:
        return getattr(current_user, "moderator", False) or getattr(current_user, "admin", False)



def can_moderate(user, forum=None, perm=None):
    """Only moderators and admins can moderate
    """

    # if the user is a super_mod or admin, he can moderate all forums
    return getattr(user, "moderator", False) or getattr(user, "admin", False)
    #return user.permissions['super_mod'] or user.permissions['admin']


def can_edit_post(user, post):
    """Check if the post can be edited by the user."""
    topic = post.topic

    if is_moderator(user):
        return True

    if topic.locked or topic.forum.locked:
        return False

    return is_authenticated(user) and post.user_id==user.id

    # return check_perm(user=user, perm='editpost', forum=post.topic.forum,
    #                   post_user_id=post.user_id)


def can_delete_post(user, post):
    """Moderators and owners of the post can delete them"""
    topic = post.topic
    if can_moderate(user, topic.forum):
        return True
    if topic.locked or topic.forum.locked:
        return False
    return is_authenticated(user) and post.user_id==user.id
    # return check_perm(user=user, perm='deletepost', forum=post.topic.forum,
    #                   post_user_id=post.user_id)


def can_delete_topic(user, topic):
    """Only moderators can delete topics"""
    if can_moderate(user, topic.forum):
        return True

    # return check_perm(user=user, perm='deletetopic', forum=topic.forum,
    #                   post_user_id=topic.user_id)


def can_post_reply(user, topic):
    """If user is authenticated and topic is not locked"""
    if can_moderate(user, topic.forum):
        return True

    if topic.locked or topic.forum.locked:
        return False

    return is_authenticated(user) and not topic.locked

    #return check_perm(user=user, perm='postreply', forum=topic.forum)


def can_post_topic(user, forum):
    """Checks if the user is allowed to create a new topic in the forum."""
    return is_authenticated(user) and not forum.locked
    # return check_perm(user=user, perm='posttopic', forum=forum)


# Moderator permission checks
def can_edit_user(user):
    """Check if the user is allowed to edit another users profile.
    Requires at least ``mod`` permissions.
    """
    return can_moderate(user=user, perm="mod_edituser")


def can_ban_user(user):
    """Check if the user is allowed to ban another user.
    Requires at least ``mod`` permissions.
    """
    return can_moderate(user=user, perm="mod_banuser")
