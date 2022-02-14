from django.core.management import BaseCommand
import pandas as pd
from app.models import Estabelecimento


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        df = pd.read_json('lais_estabelecimentos.json')
        partial_df = df[['NO_FANTASIA', 'CO_CNES']]

        for index, row in partial_df.iterrows():
            insert_info = Estabelecimento.objects.create(nome_estabelecimento= row['NO_FANTASIA'], codigo_cnes= row['CO_CNES'])
            print(f"Estabelecimento {row['NO_FANTASIA']}, {row['CO_CNES']} inserido com sucesso!")



