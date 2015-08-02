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

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_admin(current_user):
            abort(403)
        else:
            return f(*args, **kwargs)
    return decorated


def moderator_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_moderator(current_user):
            abort(403)
        else:
            return f(*args, **kwargs)
    return decorated


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
    return post_user_id and user.id and not getattr(user, is_lockdownuser, False)
        # return True
        # #need to figure someting out here
        # return user.permissions[perm] and user.id == post_user_id

    # return not user.permissions['banned'] and user.permissions[perm]


def is_moderator(user):
    """Returns ``True`` if the user is in a moderator or super moderator group.

    :param user: The user who should be checked.
    """
    return getattr(user, "moderator", False) or getattr(user, "admin", False)


def is_admin(user):
    """Returns ``True`` if the user is a administrator.

    :param user:  The user who should be checked.
    """
    return getattr(user, "admin", False)


def is_admin_or_moderator(user):
    """Returns ``True`` if the user is either a admin or in a moderator group

    :param user: The user who should be checked.
    """
    return getattr(user, "moderator", False) or getattr(user, "admin", False)


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

    return check_perm(user=user, perm='editpost', forum=post.topic.forum,
                      post_user_id=post.user_id)


def can_delete_post(user, post):
    """Check if the post can be deleted by the user."""
    return check_perm(user=user, perm='deletepost', forum=post.topic.forum,
                      post_user_id=post.user_id)


def can_delete_topic(user, topic):
    """Check if the topic can be deleted by the user."""
    return check_perm(user=user, perm='deletetopic', forum=topic.forum,
                      post_user_id=topic.user_id)


def can_post_reply(user, topic):
    """Check if the user is allowed to post in the forum."""
    if can_moderate(user, topic.forum):
        return True

    if topic.locked or topic.forum.locked:
        return False

    return check_perm(user=user, perm='postreply', forum=topic.forum)


def can_post_topic(user, forum):
    """Checks if the user is allowed to create a new topic in the forum."""
    return check_perm(user=user, perm='posttopic', forum=forum)


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
