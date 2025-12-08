from src.models.collections_models import CasinoBalance, GooseCollection, ChipCollection


def test_casino_balance(mocker, test_player):
    """Проверка занесения игрока в список казино."""
    casino_balance = CasinoBalance()
    mock_print = mocker.patch("builtins.print")
    casino_balance[test_player.name] = test_player.balance

    mock_print.assert_called_once_with("💰 Наш Игрок Тестовый Игрок обновил свой баланс с 0 на 185 ганс.")
    assert casino_balance[test_player.name] == test_player.balance


def test_goose_collection(war_goose, honk_goose):
    """Проверка списка гусей казино."""
    geese = GooseCollection()
    geese.extend([war_goose, honk_goose])
    war_geese, honk_geese = geese.get_war_geese(), geese.get_honk_geese()

    assert war_geese == [war_goose]
    assert honk_geese == [honk_goose]


def test_chip_collection_balance(chip_100, chip_50):
    """Проверка счёта суммы фишек"""
    chips = ChipCollection()
    chips.extend([chip_100, chip_50])

    assert chips.total_balance() == 150


def test_chip_collection_take_chips(chip_100, chip_50):
    """Проверка получения фишек из казино для игрока."""
    chips = ChipCollection()
    chips.extend([chip_100, chip_50])
    taken_chips = chips._take_chips_from_bank(150)

    assert taken_chips == [chip_50, chip_100]
    assert chips == []
