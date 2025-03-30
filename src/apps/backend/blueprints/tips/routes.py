from flask import flash, jsonify, request, url_for, redirect, render_template
from flask_login import current_user, login_required
from application.types import JSONResponse, RedirectRenderResponse
from application.decorators import kyc_required
from application.forms.tip_form import TipForm
from application.database.database_service import DatabaseService

from . import tips_bp


@tips_bp.route("/tips/send/<author>/<post_id>", methods=["GET"])
@login_required
@kyc_required
def _send(author: str, post_id: str) -> RedirectRenderResponse:
    post = DatabaseService.get_post(author, post_id)

    if not post:
        flash("Post not found.", "danger")
        return redirect(url_for("meta._index"))

    if author == current_user.username:
        flash("You can't tip your own post.", "danger")
        return redirect(url_for("posts._view", author=author, post_id=post_id))

    user = DatabaseService.get_user_by_username(author)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("meta._index"))

    tip_form = TipForm()
    tip_form.sender.data = current_user.address
    tip_form.sender.render_kw = {"readonly": True}
    tip_form.recipient.data = user.address
    tip_form.recipient.render_kw = {"readonly": True}

    return render_template("tips/send.html", post=post, tip_form=tip_form)


@tips_bp.route("/tips/record", methods=["POST"])
@login_required
@kyc_required
def _record() -> JSONResponse:
    data = request.get_json()
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")
    post_id = data.get("post_id")
    tx_hash = data.get("txHash")

    sender = DatabaseService.get_user_by_address(sender)
    recipient = DatabaseService.get_user_by_address(recipient)

    if not sender or not recipient:
        return jsonify({"error": "Invalid sender or recipient."}), 400

    DatabaseService.record_tip(
        sender.username, recipient.username, amount, post_id, tx_hash
    )

    return jsonify({"success": "Tip recorded."}), 200


@tips_bp.route("/tips/dashboard", methods=["GET"])
@login_required
@kyc_required
def _dashboard() -> str:
    sent_tips = DatabaseService.get_sent_tips(current_user.username)
    received_tips = DatabaseService.get_received_tips(current_user.username)

    return render_template(
        "tips/dashboard.html", sent_tips=sent_tips, received_tips=received_tips
    )
