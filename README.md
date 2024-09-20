# **Добрый день, уважаемый соискатель**

данное задание нацелено на выявление вашего реального уровня в разработке на python, поэтому отнеситесь к нему, как к работе на проекте. Выполняйте его честно и проявите себя по максимуму, удачи! 

* Напишите приложение, которое по REST принимает запрос вида

```POST api/v1/wallets/<WALLET_UUID>/operation
{
operationType: DEPOSIT or WITHDRAW,
amount: 1000
}
```

* после выполнять логику по изменению счета в базе данных
* также есть возможность получить баланс кошелька
```
GET api/v1/wallets/{WALLET_UUID}
```

## стек:

**FastAPI / Flask / Django
Postgresql**

Должны быть написаны миграции для базы данных с помощью liquibase (по желанию)
Обратите особое внимание проблемам при работе в конкурентной среде (1000 RPS по одному кошельку).
Ни один запрос не должен быть не обработан (50Х error)
Предусмотрите соблюдение формата ответа для заведомо неверных запросов, когда кошелька не существует, не валидный json, или недостаточно средств.
приложение должно запускаться в докер контейнере, база данных тоже, вся система должна подниматься с помощью docker-compose
предусмотрите возможность настраивать различные параметры приложения и базы данных без пересборки контейнеров.
эндпоинты должны быть покрыты тестами.

Решенное задание залить на гитхаб, предоставить ссылку

_Все возникающие вопросы по заданию решать самостоятельно, по своему усмотрению._
