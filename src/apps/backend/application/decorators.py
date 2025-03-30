from typing import Any, TypeVar, Callable, cast

from functools import wraps

from flask import flash, url_for, redirect
from flask_login import current_user

F = TypeVar("F", bound=Callable[..., Any])


def kyc_required(func: F) -> F:
    @wraps(func)
    def decorated_function(*args: object, **kwargs: object) -> object:
        if not current_user.verified:
            flash("Please complete your KYC first!", "warning")
            return redirect(url_for("auth._kyc"))
        return func(*args, **kwargs)

    return cast(F, decorated_function)


def admin_required(func: F) -> F:
    @wraps(func)
    def decorated_function(*args: object, **kwargs: object) -> object:
        if not current_user.admin:
            flash("You are not authorized to access this page.", "error")
            return redirect(url_for("app._index"))
        return func(*args, **kwargs)

    return cast(F, decorated_function)
