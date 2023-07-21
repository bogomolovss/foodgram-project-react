import csv
import os

from django.core.management.base import BaseCommand
from foodgram_backend.settings import BASE_DIR
from ingredients.models import Ingredient


# This format used for scalability in future
# (if we want) to import more than just Ingredients
class Command(BaseCommand):
    help = "Load data from static_folder into DB"

    def handle(self, *args, **options):
        fields_ingredients = ("name", "measurement_unit")

        files = {"ingredients.csv": (Ingredient, fields_ingredients)}

        for csv_file, (model, fieldnames) in files.items():
            file_path = os.path.join(options["path"], csv_file)
            with open(file_path, mode="r", encoding="utf-8") as file_t:
                reader = csv.DictReader(file_t)
                if fieldnames:
                    reader.fieldnames = fieldnames
                    reader = list(reader)[1:]
                else:
                    reader = list(reader)
                for row in reader:
                    obj = model.objects.create(**row)
                    obj.save()

                print(f"Импорт данных из {csv_file} выполнен успешно")

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            action="store",
            default=BASE_DIR / "static/data",
            help="Change path to import files",
        )
