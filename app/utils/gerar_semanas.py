from datetime import date, timedelta
from typing import Iterator, Tuple


def gerar_semanas(
    data_inicio: date,
    data_fim: date | None = None
) -> Iterator[Tuple[date, date]]:

    if data_fim is None:
        data_fim = date.today()

    atual = data_inicio

    while atual <= data_fim:
        fim_semana = min(atual + timedelta(days=2), data_fim)
        yield atual, fim_semana
        atual = fim_semana + timedelta(days=1)
