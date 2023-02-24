# Проект "Foodgram"

- сохраняйте любимые рецепты
- создавайте списки покупок
- подписывайтесь на других любителей пожрать

## Первый запуск

```
cd infra
sudo docker-compose up
```

## Загрузка тестовых моделей

```
python manage.py loadcsv users FoodgramUser
python manage.py loadcsv tags Tag
python manage.py loadcsv ingredients Ingredient
python manage.py make_relations
```

## Технологии

- Django
- React
- Docker
- Nginx
- PostgreSQL

## Статическая документация

- /api/ - DRF Self-describing docs
- /api/docs - Redoc

## Author

Gavin Greenhorn
