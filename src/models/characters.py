import random


class Player:
    """Класс игрока. Имеет имя, hp, свой баланс(сумма номиналов фишек) и список фишек."""

    def __init__(self, name: str) -> None:
        """Инициализация характеристик игрока."""
        self.name = name
        self.hp = 100
        self.balance = 0
        self.chips = []

    def set_balance(self) -> int:
        """Расчет текущего баланса игрока."""
        return sum(chip.value for chip in self.chips)

    def _starting_chips(self, amount: int) -> None:
        """Случайный выбор начального капитала игрока."""
        chips = [100, 50, 25, 10, 5, 1]
        while amount > 0:
            available_chips = [chip for chip in chips if chip <= amount]
            if not available_chips:
                break
            chip = random.choice(available_chips)
            amount -= chip
            self.chips.append(Chip(chip))
        self.balance = self.set_balance()

    def _chips_to_bet(self) -> tuple[list[Chip], int] | None:
        """Случайный выбор фишек для ставки игрока, если они у него есть."""
        if not self.chips:
            print("🦆 Твоя жопа гола, бро. Приходи, когда будет кэш.")
            return None

        chips_count = random.randint(1, len(self.chips))
        bet_chips = random.sample(self.chips, chips_count)

        return bet_chips, sum(chip.value for chip in bet_chips)

    def remove_chips(self, chips: list[Chip]) -> None:
        """Забирает фишки игрока после проигрыша/ограбления."""
        for chip in chips:
            if chip in self.chips:
                self.chips.remove(chip)
        self.balance = self.set_balance()

    def add_chips(self, new_chips: list[Chip]) -> None:
        """Добавляет фишки игроку после выигрыша."""
        if isinstance(new_chips, list):
            self.chips.extend(new_chips)
        else:
            self.chips.append(new_chips)
        self.balance = self.set_balance()


class Goose:
    """Класс гусей. У гуся есть имя, наглость и украденные фишки"""

    def __init__(self, name) -> None:
        """Инициализация характеристик гуся."""
        self.name = name
        self.audacity = random.randint(1, 10)
        self.stolen_chips = []

    def still_money(self, name: str) -> list[Chip]:
        """Случайный выбор суммы для кражи у игрока."""
        stolen_amount = random.randint(10, 300)
        stolen_chips = []
        chips = [1, 5, 10, 25, 50, 100]
        remaining = stolen_amount

        for chip in chips:
            while remaining >= chip:
                stolen_chips.append(Chip(chip))
                remaining -= chip

        self.stolen_chips.extend(stolen_chips)

        print(f"💸 Гусь {self.name} стырил {stolen_amount} ганс у {name}.")
        return stolen_chips

    def __add__(self, other: "Goose") -> "GooseFlock":
        """Сбор гусей в стаю."""
        return GooseFlock([self, other])


class Whore:
    def __init__(self, name: str, eye_color: str, hair_color: str) -> None:
        self.name = name
        self.eye_color = eye_color
        self.hair_color = hair_color
        self.sexuality = random.choice(list(range(1, 20)) + [999])

    def give_pleasure(self, name: str) -> list[int]:
        if self.sexuality == 999:
            return [-1]
        base_prise = self.sexuality + 5
        if self.hair_color == "блонд" and self.eye_color in ("зелёные", "голубые"):
            print(
                f"👩🏼 У девы {self.name} волосы цвета блонд и {self.eye_color} глаза. Она достойна большего.\n Время с ней обойдётся в {base_prise + 5} ганс.")
            base_prise += 5
        time_price = []
        chips = [1, 5, 10, 25, 50, 100]
        remaining = base_prise

        for chip in chips:
            while remaining >= chip:
                time_price.append(Chip(chip))
                remaining -= chip
        print(f"👩🏻‍🦰 Дева {self.name} провела время с {name}.")
        return time_price



class WarGoose(Goose):
    def son_of_bitch_attack(self, name: str) -> int:
        """Случайный урон для атаки игрока военным гусём."""
        damage = random.randint(self.audacity, 20)
        print(
            f"⚔️ {name}, дай-ка разукрасить твою физиономию, азартный ты ублюдок!. Теперь твоё личико на {damage} ударов из 100.")
        return damage


class HonkGoose(Goose):
    def honk(self, name: str) -> int:
        """Случайный уровень крика для оглушения игрока крикливым гусём."""
        honk_level = random.randint(self.audacity, 20)
        print(f"📢 Гусь {self.name} крикнул со громкостью в {honk_level} Гусебелл! И оглушил {name}.")
        return honk_level


class GooseFlock(Goose):
    def __init__(self, geese: list[Goose]) -> None:
        """Инициализация характеристик стаи гусей вместо обычных - размер стаи, имя, список гусей в стае"""
        super().__init__(geese)
        self.geese = geese
        self.size = len(geese)
        self.name = f"🦆 Стая из гусей: {[goose.name for goose in self.geese]}"

    def collab_attack(self, name: str) -> int:
        """Объединенная атака стаи гусей со случайным уроном."""
        total_damage = 0
        for goose in self.geese:
            if isinstance(goose, WarGoose):
                total_damage += goose.son_of_bitch_attack(name)
            elif isinstance(goose, HonkGoose):
                total_damage += goose.honk(name)
        return total_damage


class Chip:
    """Класс фишек. Фишка имеет свои наминал и цвет для него."""

    def __init__(self, value: int = None) -> None:
        """Инициализация наминала и цвета фишки."""
        self.value = value if value is not None else random.choice([1, 5, 10, 25, 50, 100])
