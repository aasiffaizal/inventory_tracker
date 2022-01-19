import csv
from io import StringIO

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel


def get_csv_from_orm(data: list[SQLModel]) -> StringIO:
    file_string = StringIO()
    headers = data[0].dict().keys()
    writer = csv.DictWriter(file_string, fieldnames=headers)
    writer.writeheader()
    for row in data:
        writer.writerow(jsonable_encoder(row))
    file_string.seek(0)
    return file_string
