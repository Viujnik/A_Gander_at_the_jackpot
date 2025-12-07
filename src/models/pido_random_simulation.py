import random

from src.models.casino import Casino
from src.models.characters import WarGoose, GooseFlock, HonkGoose, Player
from src.models.collections_models import PlayerCollection, GooseCollection


def player_check(player: "Player") -> bool:
    """Проверка hp и баланса игрока для удаления его из списка игроков при необходимости"""
    if player.balance <= 0:
        print(f"{player.name} забирает Гусе-полиция из-за неположительного счёта")
        return False
    if player.hp <= 0:
        print(f"{player.name}, R.I.P.")
        return False
    return True


class Actions:
    """Класс 'Действия'. Класс для хранения списка действий симуляции и функций для каждого действия."""

    def __init__(self) -> None:
        """Инициализация списка действий симуляции."""
        self.actions_list = ["players_bet", "attack_of_geese",
                             "goose_try_still_money", "goose_collab"]

    def player_bet(self, casino: "Casino", casino_players: PlayerCollection) -> None:
        """Логика для ставки игрока - случайный исход ставки, выплата фишек/потеря фишек."""
        if len(casino_players) < 1:
            print("Лохи пока не зарегистрировались у нас.")

        player = random.choice(casino_players)
        bet_chips, sum_chips = player._chips_to_bet()
        if not bet_chips:
            return
        print(f"\n🎰 {player.name} делает ставку:")
        print(f"    Ставка: {sum_chips} ганс; (Количество фишек: {len(bet_chips)})")

        player.remove_chips(bet_chips)
        casino.chips_balance.extend(bet_chips)

        if random.random() < 0.4:
            win_multiplier = random.choice([1.5, 2, 3])
            win_amount = int(sum_chips * win_multiplier)

            if win_amount <= casino.chips_balance.total_balance():
                win_chips = casino.chips_balance._take_chips_from_bank(win_amount)

                if win_chips:
                    player.add_chips(win_chips)
                    casino.balance[player.name] = player.balance
                    print(f"   ✅ Выйгрыш! x{win_multiplier}")
                    print(f"   Получено: {win_amount} ганс")
                    print(f"   Новый баланс игрока: {player.balance} ганс")
                else:
                    print(f"   🏦 Сори! Банк казино пуст")

            else:
                # Казино не может выплатить - возвращаем ставку
                print(f"   🏦 Казино не может выплатить {win_amount} ганс!")
                print(f"   Ставка будет возвращена игроку")
                player.add_chips(bet_chips)
                for chip in bet_chips:
                    if chip in casino.chips_balance:
                        casino.chips_balance.remove(chip)

        else:
            casino.balance[player.name] = player.balance
            casino.chips_balance.extend(bet_chips)

            print(f"   ❌ Проигрыш")
            print(f"   Новый баланс: {player.balance} ганс")
            print(f"   Банк казино пополнен на {sum_chips} ганс")

        check_player = player_check(player)
        if not check_player:
            casino.players.remove(player)

    def goose_attack(self, casino: "Casino", casino_geese: GooseCollection, casino_players: PlayerCollection) -> None:
        """Логика атаки гусей - на основе типа гесей выбирается случайный урон для игроков."""
        if not casino_geese or not casino_players:
            return

        goose = random.choice(casino_geese)

        if isinstance(goose, WarGoose):
            player = random.choice(casino_players)
            damage = goose.son_of_bitch_attack(player.name)
            player.hp -= damage
            check_player = player_check(player)

            if not check_player:
                casino.players.remove(player)
        elif isinstance(goose, HonkGoose):
            for _ in range(random.randint(len(casino.players), min(3, len(casino.players)))):
                player = random.choice(casino_players)
                honk_damage = goose.honk(player.name)
                player.hp -= honk_damage
                check_player = player_check(player)
                if not check_player:
                    casino.players.remove(player)
        else:
            for _ in range(random.randint(len(casino.players), min(2, len(casino.players)))):
                player = random.choice(casino_players)
                collab_damage = goose.collab_attack(player.name)
                player.hp -= collab_damage
                check_player = player_check(player)
                if not check_player:
                    casino.players.remove(player)

    def still_money(self, casino_geese: GooseCollection, casino_players: PlayerCollection) -> None:
        """Логика кражи денег гусями у игроков."""
        goose = random.choice(casino_geese)
        player = random.choice(casino_players)
        stolen_money = goose.still_money(player.name)
        player.balance -= sum(chip.value for chip in stolen_money)
        player.remove_chips(stolen_money)

    def geese_collab(self, casino_geese: GooseCollection) -> "GooseFlock":
        """Логика объединения гусей в стаю для шага симуляции."""
        goose1 = random.choice(casino_geese)
        goose2 = random.choice(casino_geese)
        return GooseFlock([goose1, goose2])
