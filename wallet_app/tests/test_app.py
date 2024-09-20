import pytest
from wallet_app.app import create_app
from wallet_app.models import db, Wallet
from wallet_app.config import Config


@pytest.fixture
def client():
    app = create_app()
    # Настройка для тестирования
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()  # Создаем базы данных
        yield app.test_client()  # Возвращаем тестовый клиент
        db.drop_all()  # Удаляем базы данных после тестов


def test_create_wallet(client):
    wallet_uuid = "123e4567-e89b-12d3-a456-426614174000"
    # Создаем кошелек
    response = client.post('/api/v1/wallets', json={'uuid': wallet_uuid})
    assert response.status_code == 201

    # Проверяем, что кошелек успешно создан
    wallet = Wallet.query.filter_by(uuid=wallet_uuid).first()
    assert wallet is not None
    assert wallet.balance == 0  # Баланс должен быть 0


def test_get_wallet(client):
    wallet_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response = client.post('/api/v1/wallets', json={'uuid': wallet_uuid})

    # Проверяем получение кошелька
    response = client.get(f'/api/v1/wallets/{wallet_uuid}')
    assert response.status_code == 200
    assert response.json['balance'] == '0'


def test_deposit_operation(client):
    wallet_uuid = "123e4567-e89b-12d3-a456-426614174000"
    client.post('/api/v1/wallets', json={'uuid': wallet_uuid})

    response = client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json={'operationType': 'DEPOSIT', 'amount': 100}
    )
    assert response.status_code == 200
    assert response.json['balance'] == '100'  # Проверяем, что баланс обновился


def test_withdraw_operation(client):
    wallet_uuid = "123e4567-e89b-12d3-a456-426614174000"
    client.post('/api/v1/wallets', json={'uuid': wallet_uuid})
    # Пополняем баланс
    client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json={'operationType': 'DEPOSIT', 'amount': 100}
    )

    response = client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json={'operationType': 'WITHDRAW', 'amount': 50}
    )
    assert response.status_code == 200
    assert response.json['balance'] == '50'  # Проверяем, что баланс обновился


def test_withdraw_insufficient_balance(client):
    wallet_uuid = "123e4567-e89b-12d3-a456-426614174000"
    client.post('/api/v1/wallets', json={'uuid': wallet_uuid})
    client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json={'operationType': 'DEPOSIT', 'amount': 30}
    )

    response = client.post(
        f'/api/v1/wallets/{wallet_uuid}/operation',
        json={'operationType': 'WITHDRAW', 'amount': 50}
    )
    assert response.status_code == 400  # Ожидаем ошибку
    assert "Недостаточно средств на счете." in response.json['message']
