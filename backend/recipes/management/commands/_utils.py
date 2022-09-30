import csv
import os
from typing import AnyStr, Dict, List, Tuple

from django.apps import apps
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


def get_csv_data(source: str, headers: Tuple) -> List[Dict]:
    """Load test data from csv as python dict."""
    with open(
        os.path.join(
            settings.BASE_DIR,
            f'static/data/{source}.csv'
        ), 'r'
    ) as file:
        csv_dict = csv.DictReader(file, fieldnames=headers)
        return [{attr: row.get(attr) for attr in row} for row in csv_dict]


def set_by_id(payload: Dict, field: AnyStr) -> None:
    """Rename incoming dict key to the foreign key name."""
    payload[f'{field}_id'] = payload.pop(field)


def load_model_data(
        app_label: str, headers: Tuple, source: str, modelname: str,
        related_field: str = None) -> None:
    """Get data from csv source, create model instances from it"""
    data = get_csv_data(source=source, headers=headers)
    model = apps.get_model(app_label, modelname)
    for payload in data:
        if related_field:
            set_by_id(payload, related_field)
        if not model.objects.filter(**payload).exists():
            if modelname == 'FoodgramUser':
                payload['is_staff'] = bool(payload['is_staff'])
            model.objects.get_or_create(**payload)


def get_image(path: str) -> SimpleUploadedFile:
    """Get an image reference for a django image field"""
    with open(path, "rb") as f:
        return SimpleUploadedFile(
            name=path,
            content=f.read(),
            content_type='image/jpg'
        )
