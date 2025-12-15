from src.models.characters import Player, GooseFlock, Chip


def test_player_model():
    """Тест стартовых характеристик игрока."""
    name = "Тестовый"
    player = Player(name)

    assert player.name == name
    assert player.hp == 100
    assert player.balance == 0
    assert player.chips == []


def test_player_add_chips(test_player, chip_100):
    """Проверка добавления фишек в список игрока."""
    starting_balance = test_player.balance
    chips_count = len(test_player.chips)
    test_player.add_chips([chip_100])

    assert len(test_player.chips) == chips_count + 1
    assert test_player.balance == starting_balance + chip_100.value
    assert chip_100 in test_player.chips


def test_player_remove_chips(test_player):
    """Проверка удаления фишек из списка игрока."""
    starting_balance = test_player.balance
    removing_chips = test_player.chips[0]
    test_player.remove_chips([removing_chips])

    assert test_player.balance == starting_balance - removing_chips.value
    assert removing_chips not in test_player.chips


def test_player_set_balance(test_player):
    """Проверка счёта баланса игрока."""
    test_player.set_balance()

    assert test_player.balance == sum(c.value for c in test_player.chips)


def test_player_no_chips_to_bet(mocker):
    """Проверка ставки игрока с нулевым балансом."""
    player = Player("Голый Игрок")
    mock_print = mocker.patch("builtins.print")
    result = player._chips_to_bet()

    mock_print.assert_called_once_with("🦆 Твоя жопа гола, бро. Приходи, когда будет кэш.")
    assert result is None


def test_goose_still_money(mocker, war_goose):
    mocker.patch("random.randint", return_value=2)
    mock_print = mocker.patch("builtins.print")
    result = [c.value for c in war_goose.still_money("Игрок")]

    mock_print.assert_called_once_with("💸 Гусь Тестовый Воин стырил 2 ганс у Игрок.")
    assert result == [Chip(1).value, Chip(1).value]


def test_war_goose_attack(mocker, war_goose):
    """Проверка атаки военного гуся."""
    mocker.patch("random.randint", return_value=99)
    mock_print = mocker.patch("builtins.print")
    damage = war_goose.son_of_bitch_attack("Игрок")

    mock_print.assert_called_once_with(
        "⚔️ Игрок, дай-ка разукрасить твою физиономию, азартный ты ублюдок!. Теперь твоё личико на 99 ударов из 100.")
    assert damage == 99


def test_honk_goose_attack(mocker, honk_goose):
    """Проверка уровня шума крикливого гуся."""
    mocker.patch("random.randint", return_value=1)
    mock_print = mocker.patch("builtins.print")
    honk_level = honk_goose.honk("Игрок")

    mock_print.assert_called_once_with("📢 Гусь Тестовый Крикун крикнул со громкостью в 1 Гусебелл! И оглушил Игрок.")
    assert honk_level == 1


def test_goose_flock(war_goose, honk_goose):
    """Проверка создания стаи."""
    flock = war_goose + honk_goose

    assert war_goose in flock.geese and honk_goose in flock.geese
    assert flock.size == 2
    assert flock.geese == [war_goose, honk_goose]
    assert flock.name == "Стая из гусей: [\'Тестовый Воин\', \'Тестовый Крикун\']"


def test_collab_attack(mocker, war_goose, honk_goose):
    """Проверка совместной атаки стаи гусей."""
    flock = GooseFlock([war_goose, honk_goose])
    mocker.patch("random.randint", side_effect=[20, 40])
    total_damage = flock.collab_attack("Игрок")

    assert total_damage == 60


def test_chip(chip_50, chip_100):
    """Проверка свойств фишек."""
    assert chip_50.value == 50
