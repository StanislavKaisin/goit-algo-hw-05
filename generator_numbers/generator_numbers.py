import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    liist_text = text.split()
    pattern = r"-?\d+\.?\d*"
    for word in liist_text:
        match = re.match(pattern, word)
        if match:
            yield float(match.group())


def sum_profit(text: str, func: Callable) -> float:
    list_numbers = func(text)
    total_sum = sum(list_numbers)
    return total_sum


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
