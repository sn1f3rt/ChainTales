import secrets

from flask import flash, url_for, redirect, render_template
from flask_login import current_user, login_required
from application.types import RedirectResponse, RedirectRenderResponse
from application.decorators import kyc_required
from application.forms.post_form import PostForm
from application.database.database_service import DatabaseService

from . import posts_bp


@posts_bp.route("/posts/me", methods=["GET"])
@login_required
@kyc_required
def _me() -> str:
    posts = DatabaseService.get_user_posts(current_user.username)

    return render_template("posts/me.html", posts=posts)


@posts_bp.route("/posts/view/<author>/<post_id>", methods=["GET"])
def _view(author: str, post_id: str) -> RedirectRenderResponse:
    post = DatabaseService.get_post(author, post_id)

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("meta._index"))

    return render_template("posts/view.html", post=post)


@posts_bp.route("/posts/new", methods=["GET", "POST"])
@login_required
@kyc_required
def _new() -> RedirectRenderResponse:
    post_form = PostForm()

    if post_form.validate_on_submit():
        post_id = secrets.token_hex(4)

        DatabaseService.new_post(
            current_user.username,
            post_id,
            post_form.title.data or "",
            post_form.content.data or "",
        )

        flash("Post created.", "success")
        return redirect(url_for("posts._me"))

    return render_template("posts/new.html", post_form=post_form)


@posts_bp.route("/posts/update/<author>/<post_id>", methods=["GET", "POST"])
@login_required
@kyc_required
def _update(author: str, post_id: str) -> RedirectRenderResponse:
    post = DatabaseService.get_post(author, post_id)

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("posts._me"))

    post_form = PostForm()

    if post_form.validate_on_submit():
        DatabaseService.update_post(
            author, post_id, post_form.title.data or "", post_form.content.data or ""
        )

        flash("Post updated.", "success")
        return redirect(url_for("posts._view", author=author, post_id=post_id))

    post_form.title.data = post.title
    post_form.content.data = post.content

    return render_template("posts/update.html", post_id=post.id, post_form=post_form)


@posts_bp.route("/posts/delete/<author>/<post_id>", methods=["GET"])
@login_required
@kyc_required
def _delete(author: str, post_id: str) -> RedirectResponse:
    post = DatabaseService.get_post(author, post_id)

    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("posts._me"))

    DatabaseService.delete_post(author, post_id)

    flash("Post deleted.", "success")
    return redirect(url_for("posts._me"))
