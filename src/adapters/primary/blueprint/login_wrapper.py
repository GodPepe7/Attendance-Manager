import functools

from flask import g, session, request, redirect, url_for


def login_required():
    """View decorator that blocks access to sites if not logged in."""

    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                if request.endpoint != "index":
                    session['next'] = request.url
                return redirect(url_for('auth.login'))

            return view(**kwargs)

        return wrapped_view

    return decorator
