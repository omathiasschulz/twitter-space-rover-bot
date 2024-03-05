from datetime import datetime


def date_describe(base_date: str) -> str:
    """Formata a data e retorna no padrão: DD de FULL_MM de YYYY

    Args:
        base_date (str): Data para formatar no padrão YYYY-MM-DD

    Returns:
        str: Retorna a data formatada
    """
    full_months = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro",
    }
    date = datetime.strptime(base_date, "%Y-%m-%d")
    month = date.strftime("%m")
    return date.strftime(f"%d de {full_months[month]} de %Y")
