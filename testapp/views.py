"""
=============
testapp.views
=============

View functions for Comments app.

"""

from flask import (
    current_app,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import storage

from constants import USERNAME_KEY
from decorators import username_required
from utils import to_index, to_threads


@username_required
def comment(thread_uid):
    """Add new comment to given thread.

    :param thread: Thread unique ID.
    """
    thread = storage.get_thread(thread_uid)
    if not thread:
        return error(404)

    text = request.form.get('text') or ''
    if not text:
        return error('comment:text')

    storage.add_comment(thread_uid, g.username, text)
    flash('Your comment successfully added!', 'success')

    return redirect(url_for('comments', thread_uid=thread_uid))


@username_required
def comments(thread_uid):
    """List all comments in given thread.

    :param thread_uid: Thread unique ID.
    """
    thread = storage.get_thread(thread_uid, counter=True)
    if not thread:
        return error(404)
    return render_template('comments.html',
                           comments=storage.list_comments(thread_uid),
                           thread=thread,
                           thread_uid=thread_uid)


@username_required
def delete_thread(thread_uid):
    """Delete given thread and all its comments.

    :param thread_uid: Thread unique ID.
    """
    thread = storage.get_thread(thread_uid)
    if not thread:
        return error(404)

    if thread['author'] != g.username:
        return error(403)

    if request.method == 'GET':
        return render_template('delete_thread.html',
                               thread=thread,
                               thread_uid=thread_uid)

    if request.form.get('confirm') != 'confirm':
        return error('delete_thread:confirm')

    storage.delete_thread(thread_uid)
    flash('Thread Succesfully Deleted: {0}'.format(thread['subject']),
          'success')

    return to_threads()


def error(code):
    """Show error page for HTTP and form errors."""


def index():
    """Setup username and log into the Comments app."""
    error = None

    # Username already supplied, redirect to threads list
    if g.username:
        return to_threads()

    if request.method == 'POST':
        username = request.form.get('username') or ''
        if len(username) > 2:
            prefix = current_app.config['KEY_PREFIX']
            username_key = USERNAME_KEY.format(prefix)
            session[username_key] = username

            flash('Welcome, {0}!'.format(username), 'success')
            return to_threads()

        error = True

    status = 400 if error else 200
    return make_response(render_template('index.html', error=error), status)


def quit():
    """Clear username from session and quit from Comments app."""
    username_key = USERNAME_KEY.format(current_app.config['KEY_PREFIX'])
    session.pop(username_key, None)
    return to_index()


@username_required
def start_thread():
    """Start new thread with or without first comment."""
    subject = request.form.get('subject') or ''
    comment = request.form.get('comment') or ''
    if not subject:
        return error('start_thread:subject')

    storage.start_thread(g.username, subject, comment)
    flash('New Thread Started: {0}'.format(subject), 'success')

    return to_threads()


@username_required
def threads():
    """List all available threads."""
    return render_template('threads.html', threads=storage.list_threads())
