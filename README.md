# Автотесты для saucedemo.com (Selenium + pytest)

## Установка
```
pip install -r requirements.txt
```

## Запуск
```
pytest                                   # Chrome по умолчанию
pytest --browser=firefox
pytest --browser=edge
pytest --browser=chrome --headless
pytest --url=https://www.saucedemo.com/
```

Скрипт без pytest: `python purchase_script.py`
