from datetime import date, timedelta
from typing import Set

class CalculadoraPrazos:
    """Regra de negócio pura para contagem de prazos processuais (CPC / dias úteis)."""

    def __init__(self, feriados: Set[date] = None):
        self.feriados = feriados or set()

    def e_dia_util(self, dt: date) -> bool:
        if dt.weekday() >= 5:  # Sábado / Domingo
            return False
        if dt in self.feriados:
            return False
        return True

    def calcular_data_fatal(self, data_disponibilizacao: date, dias_uteis: int) -> date:
        # Considera-se intimado no 1º dia útil seguinte à disponibilização
        data_intimacao = data_disponibilizacao + timedelta(days=1)
        while not self.e_dia_util(data_intimacao):
            data_intimacao += timedelta(days=1)

        # Início da contagem no 1º dia útil após a intimação
        curr = data_intimacao + timedelta(days=1)
        contagem = 0

        while contagem < dias_uteis:
            if self.e_dia_util(curr):
                contagem += 1
            if contagem == dias_uteis:
                break
            curr += timedelta(days=1)

        return curr