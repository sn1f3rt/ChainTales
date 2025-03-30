from flask import render_template
from application.database.database_service import DatabaseService

from . import meta_bp


@meta_bp.route("/", methods=["GET"])
def _index() -> str:
    posts = DatabaseService.get_latest_posts()

    return render_template("meta/index.html", posts=posts)
