from collections import UserDict, UserList

from src.models.characters import WarGoose, HonkGoose, Chip


class CasinoBalance(UserDict):
    """Словарь для хранения балансов игроков в казино."""

    def __setitem__(self, key: str, value: int) -> None:
        """Переопределение классического метода для вывода информации."""
        old_balance = self.get(key, 0)
        super().__setitem__(key, value)
        print(f"💰 Наш Игрок {key} обновил свой баланс с {old_balance} на {value} ганс.")


class PlayerCollection(UserList):
    """Список игроков казино."""
    pass

class WhoreCollection(UserList):
    """Список дев казино."""


class GooseCollection(UserList):
    """Список гусей казино."""

    def get_war_geese(self) -> list[WarGoose]:
        """Получение всех военных гусей казино"""
        return [g for g in self if isinstance(g, WarGoose)]

    def get_honk_geese(self) -> list[HonkGoose]:
        """Получение всех крикливых гусей казино"""
        return [g for g in self if isinstance(g, HonkGoose)]


class ChipCollection(UserList):
    """Список для хранения фишек казино."""

    def total_balance(self) -> int:
        return sum(chip.value for chip in self)

    def _take_chips_from_bank(self, amount: int) -> list[Chip]:
        """Получение фишек казино для выдачи их игроку."""
        if amount <= 0 or not self:
            return []

        taken_chips = []
        remaining = amount
        sorted_chips = sorted(self, key=lambda x: x.value)

        for chip in sorted_chips[:]:
            if chip.value <= remaining:
                taken_chips.append(chip)
                remaining -= chip.value
                self.remove(chip)

            if remaining <= 0:
                break

        return taken_chips
