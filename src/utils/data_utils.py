import pandas as pd
"""
como um prototypo obter os dados de um csv num futuro de uma databse    
Espera colunas: user_id, patient_name patient_description
"""

class DataUtils:
    def __init__(self, csv_path: str):
        """
        Inicializa a classe carregando o CSV com pandas.
        Espera colunas: user_id, patient_name, patient_diseases, patient_description
        """
        self.df = pd.read_csv(csv_path)
        # Garantir que user_id é string
        self.df['user_id'] = self.df['user_id'].astype(str)

    def get_patient_name(self, user_id: str) -> str:
        """Retorna o nome do paciente dado o user_id"""
        row = self.df[self.df['user_id'] == str(user_id)]
        if not row.empty:
            return row.iloc[0]['patient_name']
        return None

    def get_patient_diseases(self, user_id: str) -> str:
        """Retorna as doenças do paciente dado o user_id"""
        row = self.df[self.df['user_id'] == str(user_id)]
        if not row.empty:
            return row.iloc[0]['patient_diseases']
        return None

    def get_patient_description(self, user_id: str) -> str:
        """Retorna a descrição do paciente dado o user_id"""
        row = self.df[self.df['user_id'] == str(user_id)]
        if not row.empty:
            return row.iloc[0]['patient_description']
        return None

    def get_full_patient_info(self, user_id: str) -> dict:
        """Retorna todas as informações do paciente como um dicionário"""
        row = self.df[self.df['user_id'] == str(user_id)]
        if not row.empty:
            return {
                "patient_name": row.iloc[0]['patient_name'],
                "patient_diseases": row.iloc[0]['patient_diseases'],
                "patient_description": row.iloc[0]['patient_description']
            }
        return None
