from flask import Blueprint, request, jsonify
from .models import db, Wallet

wallet_bp = Blueprint('wallet_bp', __name__)


@wallet_bp.route('/api/v1/wallets/<string:wallet_uuid>/operation', methods=['POST'])
def operate_wallet(wallet_uuid):
    data = request.json
    if not data or 'operationType' not in data or 'amount' not in data:
        return jsonify({'error': 'Неверный формат запроса.'}), 400

    operation_type = data['operationType']
    amount = data['amount']

    wallet = Wallet.query.get(wallet_uuid)
    if not wallet:
        return jsonify({'error': 'Кошелек не существует.'}), 404

    try:
        if operation_type == 'DEPOSIT':
            wallet.deposit(amount)
        elif operation_type == 'WITHDRAW':
            wallet.withdraw(amount)
        else:
            return jsonify({'error': 'Неверный тип операции.'}), 400

        db.session.commit()
        return jsonify({'balance': str(wallet.balance)}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Ошибка обработки операции.'}), 500


@wallet_bp.route('/api/v1/wallets/<string:wallet_uuid>', methods=['GET'])
def get_wallet_balance(wallet_uuid):
    wallet = Wallet.query.get(wallet_uuid)
    if not wallet:
        return jsonify({'error': 'Кошелек не существует.'}), 404
    return jsonify({'balance': str(wallet.balance)}), 200