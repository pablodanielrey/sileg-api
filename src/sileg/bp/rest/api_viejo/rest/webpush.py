
from flask import Blueprint, request, jsonify

from sileg.model.WebPushModel import WebPushModel
from sileg.model import obtener_session

bp = Blueprint('webpush', __name__, url_prefix='/gelis/api/v1.0')

@bp.route('/info', methods=['GET'])
def info():
    pk = WebPushModel.public_key()
    return jsonify({'status':200, 'key':pk})

@bp.route('/subscribe', methods=['GET'])
def subscribe():
    subscription_info = request.json.get('subscription_info')
    # if is_active=False == unsubscribe
    is_active = request.json.get('is_active')

    with obtener_session() as session:
        sid = WebPushModel.subscribe(session, subscription_info, is_active)
        session.commit()
        return jsonify({'status':200, 'id': sid})

@bp.route('/broadcast', methods=['POST'])
def broadcast():
    message = request.json.get('message')
    with obtener_session() as session:
        count = WebPushModel.broadcast(session, message)
    return jsonify({'count':count})


