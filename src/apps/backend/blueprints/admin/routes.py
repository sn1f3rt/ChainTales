import io

from flask import abort, flash, url_for, redirect, send_file, render_template
from flask_login import current_user, login_required
from application.types import RedirectResponse, RedirectRenderResponse
from application.decorators import admin_required
from application.database.database_service import DatabaseService

from . import admin_bp


@admin_bp.route("/admin", methods=["GET"])
@login_required
def _index() -> RedirectRenderResponse:
    if not current_user.admin:
        return redirect(url_for("app._index"))

    unverified_users = DatabaseService.get_unverified_users()

    return render_template("admin/index.html", unverified_users=unverified_users)


@admin_bp.route("/admin/approve/<address>", methods=["GET"])
@login_required
def _approve(address: str) -> RedirectResponse:
    if not current_user.admin:
        return redirect(url_for("app._index"))

    DatabaseService.approve_user(address)
    flash("User approved.", "success")
    return redirect(url_for("admin._index"))


@admin_bp.route("/admin/reject/<address>", methods=["GET"])
@login_required
def _reject(address: str) -> RedirectResponse:
    if not current_user.admin:
        return redirect(url_for("app._index"))

    DatabaseService.reject_user(address)
    flash("User rejected.", "error")
    return redirect(url_for("admin._index"))


@admin_bp.route("/admin/render_id/front/<address>", methods=["GET"])
@login_required
@admin_required
def _render_id_front(address: str) -> RedirectResponse:
    if not current_user.admin:
        return redirect(url_for("app._index"))

    user = DatabaseService.get_user_by_address(address)

    if user and user.id_front:
        return send_file(
            io.BytesIO(user.id_front),
            mimetype="image/jpeg",
            as_attachment=False,
            download_name=f"{user.username}_id_front.jpg",
        )

    return abort(404)


@admin_bp.route("/admin/render_id/back/<address>", methods=["GET"])
@login_required
@admin_required
def _render_id_back(address: str) -> RedirectResponse:
    user = DatabaseService.get_user_by_address(address)

    if user and user.id_back:
        return send_file(
            io.BytesIO(user.id_back),
            mimetype="image/jpeg",
            as_attachment=False,
            download_name=f"{user.username}_id_back.jpg",
        )

    return abort(404)
