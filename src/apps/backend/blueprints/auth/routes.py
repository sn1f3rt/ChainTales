from datetime import UTC, datetime

from siwe import SiweMessage, ISO8601Datetime, generate_nonce
from flask import flash, jsonify, request, url_for, redirect, render_template
from flask_login import login_user, logout_user, current_user, login_required
from application.types import JSONResponse, RedirectResponse, RedirectRenderResponse
from application.factory import w3
from application.forms.kyc_form import KYCForm
from application.forms.username_form import UsernameForm
from application.database.database_service import DatabaseService

from . import auth_bp


@auth_bp.route("/auth/nonce/<address>", methods=["GET"])
def _nonce(address: str) -> JSONResponse:
    address = w3.to_checksum_address(address)
    user = DatabaseService.get_user_by_address(address)

    if user:
        return jsonify({"nonce": user.nonce}), 200

    nonce = generate_nonce()

    DatabaseService.add_user(address, nonce)

    return jsonify({"nonce": nonce}), 200


@auth_bp.route("/auth/message/<address>", methods=["GET", "POST"])
def _message(address: str) -> JSONResponse:
    address = w3.to_checksum_address(address)
    user = DatabaseService.get_user_by_address(address)

    if not user:
        return jsonify({"error": "No nonce found for this address."}), 400

    data = request.get_json()
    domain = data.get("domain")
    statement = data.get("statement")
    origin = data.get("origin")
    version = data.get("version")
    chain_id = data.get("chain_id")
    nonce = data.get("nonce")

    message = SiweMessage(
        domain=domain,
        address=address,
        statement=statement,
        uri=origin,
        version=version,
        chain_id=chain_id,
        issued_at=ISO8601Datetime(datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")),
        nonce=nonce,
    )

    return jsonify({"message": message.prepare_message()}), 200


@auth_bp.route("/auth/verify/<address>", methods=["POST"])
def _verify(address: str) -> JSONResponse:
    address = w3.to_checksum_address(address)
    user = DatabaseService.get_user_by_address(address)

    if not user:
        return jsonify({"error": "No nonce found for this address."}), 400

    data = request.get_json()
    message = data.get("message")
    signature = data.get("signature")

    message = SiweMessage.from_message(message)

    try:
        message.verify(signature=signature, nonce=user.nonce)

    except Exception as e:
        return jsonify({"status": "error", "message": e.__str__()}), 400

    if not user.active:
        user = DatabaseService.activate_user(address)

    login_user(user)
    flash("You have been logged in.", "success")

    tips = DatabaseService.get_pending_tips(current_user.username)

    if tips:
        for tip in tips:
            DatabaseService.mark_notified(tip.id)
            flash(
                f"You received a tip of {tip.amount} ETH from {tip.sender}.", "info"
            )

    return jsonify({"username": user.username}), 200


@auth_bp.route("/auth/username/", methods=["GET", "POST"])
@login_required
def _username() -> RedirectRenderResponse:
    if current_user.username:
        return redirect(url_for("app._index"))

    username_form = UsernameForm()

    if username_form.validate_on_submit():
        if DatabaseService.check_username(username_form.username.data or ""):
            flash("Username already taken.", "warning")
            return redirect(url_for("auth._username"))

        DatabaseService.update_username(
            current_user.address, username_form.username.data or ""
        )

        flash("Username updated successfully.", "success")

        return redirect(url_for("app._index"))

    return render_template("auth/username.html", username_form=username_form)


@auth_bp.route("/auth/logout", methods=["GET"])
@login_required
def _logout() -> RedirectResponse:
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for("meta._index"))


@auth_bp.route("/auth/settings", methods=["GET", "POST"])
@login_required
def _settings() -> RedirectRenderResponse:
    username_form = UsernameForm()

    if username_form.validate_on_submit():
        if current_user.username == username_form.username.data:
            flash("Old and new username cannot be the same.", "warning")
            return redirect(url_for("auth._settings"))

        if DatabaseService.check_username(username_form.username.data or ""):
            flash("Username already taken.", "warning")
            return redirect(url_for("auth._settings"))

        DatabaseService.update_username(
            current_user.address, username_form.username.data or ""
        )
        flash("Username updated successfully.", "success")
        return redirect(url_for("auth._settings"))

    return render_template("auth/settings.html", username_form=username_form)


@auth_bp.route("/auth/kyc", methods=["GET", "POST"])
@login_required
def _kyc() -> RedirectRenderResponse:
    kyc_form = KYCForm()

    if kyc_form.validate_on_submit():
        DatabaseService.update_kyc_info(
            current_user.address,
            kyc_form.name.data or "",
            kyc_form.age.data or "",
            kyc_form.location.data or "",
            kyc_form.id_number.data or "",
            kyc_form.id_front.data.read() if kyc_form.id_front.data else None,
            kyc_form.id_back.data.read() if kyc_form.id_back.data else None,
        )

        flash("Your KYC has been submitted for verification.", "success")
        return redirect(url_for("auth._kyc"))

    return render_template("auth/kyc.html", kyc_form=kyc_form)


@auth_bp.route("/auth/kyc/revoke", methods=["GET"])
@login_required
def _kyc_revoke() -> RedirectResponse:
    DatabaseService.revoke_kyc(current_user.address)

    flash("Your KYC has been revoked.", "warning")
    return redirect(url_for("auth._kyc"))
