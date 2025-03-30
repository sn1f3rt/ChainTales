from typing import Optional

from datetime import datetime

import click
from web3 import Web3
from flask import Flask, flash
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask_login import LoginManager, current_user

from application.types import RedirectResponse, RedirectResponseOptional
from application.config.config_service import ConfigService
from application.database.database_service import DatabaseService
from application.database.models.database_models import User

csrf: CSRFProtect
w3: Web3


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_url_path="/assets",
        static_folder="../../../assets",
        template_folder="../../frontend",
    )
    CORS(app, allow_origin="*")
    app.config.update(
        SECRET_KEY=ConfigService.get(key="app.secret_key"),
        TESTING=ConfigService.get(key="app.testing"),
        RECAPTCHA_PUBLIC_KEY=ConfigService.get(key="recaptcha.site_key"),
        RECAPTCHA_PRIVATE_KEY=ConfigService.get(key="recaptcha.secret_key"),
    )

    global csrf
    csrf = CSRFProtect()
    csrf.init_app(app)

    global w3
    w3 = Web3(Web3.HTTPProvider(ConfigService.get(key="web3.provider")))

    DatabaseService.setup_database()

    login_manager = LoginManager()
    login_manager.init_app(app)

    with app.app_context():

        @login_manager.user_loader
        def _load_user(address: str) -> Optional[User]:
            return DatabaseService.load_user(address)

        @login_manager.unauthorized_handler
        def _unauthorized() -> RedirectResponse:
            from flask import flash, url_for, redirect

            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("meta._index"))

        @app.before_request
        def _before_request() -> None:
            if hasattr(
                current_user, "address"
            ) and DatabaseService.pending_notification(current_user.address):
                if DatabaseService.get_kyc_status(current_user.address) == -1:
                    flash("Your KYC has been rejected.", "error")
                else:
                    flash(f"Your KYC has been verified and approved.", "success")

                DatabaseService.reset_kyc_status(current_user.address)

        @app.template_filter("format")
        def _format(dt: datetime) -> str:
            return dt.strftime("%Y-%m-%d %H:%M:%S")

        @app.template_filter("truncate")
        def _truncate(text: str, length: int = 50) -> str:
            return text[:length] + "..." if len(text) > length else text

        @app.template_filter("markdown")
        def _markdown(text: str) -> str:
            from markdown import markdown

            return markdown(text)

        @app.cli.command("add_admin")
        @click.argument("username")
        def _make_admin(username: str) -> None:
            if not DatabaseService.get_user_by_username(username):
                click.echo("User not found.")
                return

            DatabaseService.add_admin(username)
            click.echo(f"User {username} has been made an admin.")

        @app.cli.command("remove_admin")
        @click.argument("username")
        def _remove_admin(username: str) -> None:
            if not DatabaseService.get_user_by_username(username):
                click.echo("User not found.")
                return

            DatabaseService.remove_admin(username)
            click.echo(f"User {username} has been removed from admin.")

        @app.before_request
        def _check_username_set() -> RedirectResponseOptional:
            from flask import request, url_for, redirect
            from flask_login import current_user

            if request.endpoint in ["auth._username", "auth._logout", "static"]:
                return None

            if current_user.is_authenticated and not current_user.username:
                return redirect(url_for("auth._username"))

            return None

    from blueprints.app import app_bp
    from blueprints.auth import auth_bp
    from blueprints.meta import meta_bp
    from blueprints.tips import tips_bp
    from blueprints.admin import admin_bp
    from blueprints.posts import posts_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(app_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(meta_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(tips_bp)

    csrf.exempt("blueprints.auth.routes._message")
    csrf.exempt("blueprints.auth.routes._verify")
    csrf.exempt("blueprints.admin.routes._record")
    csrf.exempt("blueprints.tips.routes._record")

    return app
