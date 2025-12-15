import random

random.seed(5)
from src.models.characters import Chip, Player, WarGoose, HonkGoose, Goose, Whore
from src.models.collections_models import CasinoBalance, PlayerCollection, GooseCollection, ChipCollection, \
    WhoreCollection
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
whore_names = [
    "Виктория Версаче",
    "Анастасия Вольц",
    "Жасмин Леруа",
    "Кармен Диаз",
    "Шарлотта Делакур",
    "Эвелин Сент-Клер",
    "Мишель Дюваль",
    "Изабель Валентино",
    "София Ламбор",
    "Скарлетт Монтроуз",
    "Женевьева Флер",
    "Бьянка Росси",
    "Люси Фокс",
    "Мадлен Бушар",
    "Габриэлла Костелло",
    "Ванесса Рено",
    "Оливия Черчилль",
    "Николь Ларош",
    "Даниэль Мартел",
    "Кэндис Престон",
    "Леа Морган",
    "Саманта Блэк",
    "Ариэль Стил",
    "Роксана Вегас",
    "Джессика Голд",
    "Кира Найтлинг",
    "Моника Беллуччини",
    "Татьяна Орлова",
    "Ева Свон",
    "Эмбер Рояль"
]
eye_colors = ["зелёные", "голубые", "карие", "серые"]
hair_colors = ["блонд", "брюнетка", "русые", "рыжий", "каштановые"]

class Casino:
    """Класс казино. Казино имеет название, баланс, список игроков и гусей, список фишек."""

    def __init__(self) -> None:
        """Инициализация стартовых характеристик казино."""
        self.name = "Взгляд на Джекпот"
        self.balance = CasinoBalance()
        self.players = PlayerCollection()
        self.whores = WhoreCollection()
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
        print(f"🏦 Банк казино: {total_sum} ганс.")

    def player_register(self) -> "Player":
        """Регистрирует нового случайного игрока."""
        player = Player(random.choice(names))
        print(f"👤 Зарегистрирован: {player.name}")
        player._starting_chips(random.randint(500, 2000))
        self.players.append(player)
        self.balance[player.name] = player.balance
        return player

    def whore_register(self) -> "Whore":
        """Регистрирует новую случайную деву."""
        whore = Whore(random.choice(whore_names), random.choice(eye_colors), random.choice(hair_colors))
        print(f"👤 Зарегистрирована дева: {whore.name}")
        self.whores.append(whore)
        return whore

    def goose_register(self, type_of_goose: str) -> "Goose":
        """Регистрирует нового случайного гуся на основе переданного типа."""
        if type_of_goose == "war" or (type_of_goose == "random" and random.choice([True, False])):
            goose = WarGoose(random.choice(names))
            print(f"⚔️ Зарегистрирован военный гусь: {goose.name}; Наглость: {goose.audacity})")
        else:
            goose = HonkGoose(random.choice(names))
            print(f"📢 Зарегистрирован крикливый гусь: {goose.name}; Наглость: {goose.audacity})")

        self.geese.append(goose)
        return goose
    def info(self):
        if self.geese:
            print("Балансы гусей:")
            for goose in self.geese:
                print(f"🦆   {goose.name}: {sum(chip.value for chip in goose.stolen_chips)}")
        if self.players:
            print("Балансы игроков:")
            for player in self.players:
                print(f"👤   {player.name}: {player.balance}")
        print("Балансы дев")
        for whore in self.whores:
            print(f"👩🏻‍🦰   {whore.name}: {whore.balance}")

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
            case "whore_time":
                simulate.whore_time(self.whores, self.players)


def run_simulation(user_list) -> None:
    gander_casino = Casino()
    for _ in range(user_list[0]):
        gander_casino.player_register()
        gander_casino.whore_register()
        gander_casino.goose_register("war")
        gander_casino.goose_register("honk")
    for _ in range(user_list[1]):
        gander_casino.simulation_action()
    user_choise = input("Вы хотите вывести сводку балансов?(\'да\' для подтверждения, любая другая последовательность для отказа): ")
    if user_choise == "да":
        gander_casino.info()
