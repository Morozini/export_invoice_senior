from datetime import date, timedelta
from typing import Iterator, Tuple


def gerar_semanas(
    data_inicio: date,
    data_fim: date
) -> Iterator[Tuple[date, date]]:
    atual = data_inicio

    while atual <= data_fim:
        fim_semana = min(atual + timedelta(days=6), data_fim)
        yield atual, fim_semana
        atual = fim_semana + timedelta(days=1)
