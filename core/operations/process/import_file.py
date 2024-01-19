import pandas as pd

class DataImporter:
    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type

    def import_data(self):
        if self.file_type == 'csv':
            return self.import_csv()
        elif self.file_type == 'xlsx':
            return self.import_excel()
        else:
            raise ValueError("Tipo de arquivo não é suportado")

    def import_csv(self):
        try:
            data = pd.read_csv(self.file_path)
            return data
        except Exception as e:
            raise ValueError(f"Erro ao importar arquivo CSV: {str(e)}")

    def import_excel(self):
        try:
            data = pd.read_excel(self.file_path, engine='openpyxl')
            return data
        except Exception as e:
            raise ValueError(f"Erro ao importar arquivo Excel: {str(e)}")