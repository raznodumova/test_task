from flask import Flask
from config import Config
from models import db
from routes import wallet_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация БД
    db.init_app(app)

    with app.app_context():
        # Создание таблиц, если они еще не существуют
        db.create_all()

    # Регистрация маршрутов
    app.register_blueprint(wallet_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)