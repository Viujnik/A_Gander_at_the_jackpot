import random

random.seed(5)
from src.models.characters import Chip, Player, WarGoose, HonkGoose, Goose
from src.models.collections_models import CasinoBalance, PlayerCollection, GooseCollection, ChipCollection
from src.models.pido_random_simulation import Actions

names = [
    "Игорь Сидоров",
    "Анна Морозова",
    "Владимир Кузнецов",
    "Елена Смирнова",
    "Дмитрий Орлов",
    "Ольга Зайцева",
    "Михаил Попов",
    "Наталья Волкова",
    "Сергей Николаев",
    "Татьяна Павлова",
    "Андрей Семёнов",
    "Юлия Козлова",
    "Алексей Фёдоров",
    "Светлана Лебедева",
    "Павел Макаров",
    "Ксения Новикова",
    "Евгений Васильев",
    "Анастасия Иванова",
    "Артём Соловьёв",
    "Дарья Петрова",
    "Джованни Риччи",
    "Хуан Карлос",
    "Жан-Клод Дюбуа",
    "Ханс Мюллер",
    "Джон Смит",
    "Мария Гарсия",
    "Чжан Вэй",
    "София Лоренц",
    "Раджив Капур",
    "Фатима Аль-Хашими",
    "Джек Блэк",
    "Артур Король",
    "Эдди Фишка",
    "Борис Блэкджек",
    "Роман Рулетка"
]


class Casino:
    """Класс казино. Казино имеет название, баланс, список игроков и гусей, список фишек."""

    def __init__(self) -> None:
        """Инициализация стартовых характеристик казино."""
        self.name = "Взгляд на Джекпот"
        self.balance = CasinoBalance()
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.chips_balance = ChipCollection()
        self._set_casino_balance()

    def _set_casino_balance(self) -> None:
        """Заполняет стартовый баланс казино фишками."""
        chips = [100, 50, 25, 10, 5, 1]
        for chip in chips:
            for _ in range(200):
                self.chips_balance.append(Chip(chip))

        total_sum = self.chips_balance.total_balance()
        print(f"🏦Банк казино: {total_sum} ганс.")

    def player_register(self) -> "Player":
        """Регистрирует нового случайного игрока."""
        player = Player(random.choice(names))
        print(f"👤 Зарегистрирован: {player.name}")
        player._starting_chips(random.randint(500, 2000))
        self.players.append(player)
        self.balance[player.name] = player.balance
        return player

    def goose_register(self, type_of_goose: str) -> "Goose":
        """Регистрирует нового случайного гуся на основе переданного типа."""
        if type_of_goose == "war" or (type_of_goose == "random" and random.choice([True, False])):
            goose = WarGoose(random.choice(names))
            print(f"⚔️ Зарегистрирован военный гусь: {goose.name}; Наглость: {goose.audacity})")
        else:
            goose = HonkGoose(random.choice(names))
            print(f"📢 Зарегистрирован крикливый гусь: {goose.name}; Наглость {goose.audacity})")

        self.geese.append(goose)
        return goose

    def simulation_action(self) -> None:
        """Случайное действие для симуляции"""
        simulate = Actions()
        action = random.choice(simulate.actions_list)
        match action:
            case "players_bet":
                simulate.player_bet(self, self.players)
            case "attack_of_geese":
                simulate.goose_attack(self, self.geese, self.players)
            case "goose_try_still_money":
                simulate.still_money(self.geese, self.players)
            case "goose_collab":
                self.geese.append(simulate.geese_collab(self.geese))


gander_casino = Casino()
gander_casino.player_register()
gander_casino.goose_register("war")
gander_casino.player_register()
gander_casino.goose_register("honk")
for _ in range(10):
    gander_casino.simulation_action()
