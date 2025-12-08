import pytest

from src.models.characters import Player, Goose, WarGoose, HonkGoose, GooseFlock
from src.models.pido_random_simulation import player_check, Actions


def test_check_player(mocker):
    player = Player("Тестовый Игрок")
    mock_print = mocker.patch("builtins.print")
    check = player_check(player)

    mock_print.assert_called_once_with(f"🚔 Тестовый Игрок забирает Гусе-полиция из-за неположительного счёта.")
    assert check is False


@pytest.mark.parametrize("random_value, expected_capsys, check_add_chips", [
    (0.4, "Выйгрыш! x1.5", True),
    (0.5, "Проигрыш", False),
])
def test_player_bet_win(mocker, empty_casino, chip_50, chip_100, capsys, random_value, expected_capsys,
                        check_add_chips):
    mock_player = mocker.Mock()
    mock_player.name = "Игрок"
    mock_player.balance = 100
    mock_player.hp = 100
    mock_player.chips = [chip_100]
    mock_player._chips_to_bet.return_value = ([chip_100], 100)
    empty_casino.players.append(mock_player)
    simulate = Actions()

    mock_casino_chips = mocker.Mock()
    mock_casino_chips.total_balance.return_value = 1000
    mock_casino_chips._take_chips_from_bank.return_value = [chip_50, chip_100]
    empty_casino.chips_balance = mock_casino_chips

    mocker.patch("random.random", return_value=random_value)
    mocker.patch("random.choice", side_effect=[mock_player, 1.5])

    simulate.player_bet(empty_casino, empty_casino.players)

    captured = capsys.readouterr()
    assert expected_capsys in captured.out
    if check_add_chips:
        mock_player.add_chips.assert_called_once_with(empty_casino.chips_balance._take_chips_from_bank(150))


@pytest.mark.parametrize("goose_type", [
    "war", "honk", "flock"
])
def test_goose_attack(mocker, empty_casino, goose_type):
    simulate = Actions()

    mock_player = mocker.Mock()
    mock_player.name = "Игрок"
    mock_player.balance = 100
    mock_player.hp = 100

    if goose_type == "war":
        mock_goose = mocker.Mock(spec=WarGoose)
        mock_goose.name = "Военный гусь"
        mock_goose.son_of_bitch_attack.return_value = 20
    elif goose_type == "honk":
        mock_goose = mocker.Mock(spec=HonkGoose)
        mock_goose.name = "Крикливый гусь"
        mock_goose.honk.return_value = 20
    else:
        mock_goose = mocker.Mock(spec=GooseFlock)
        mock_goose.name = "Стая гусей"
        mock_goose.collab_attack.return_value = 20

    empty_casino.players.append(mock_player)
    empty_casino.geese.append(mock_goose)

    mocker.patch("random.randint", return_value=1)
    mocker.patch("random.choice", side_effect=[mock_goose, mock_player])

    simulate.goose_attack(empty_casino, empty_casino.geese, empty_casino.players)

    if goose_type == "war":
        mock_goose.son_of_bitch_attack.assert_called_once_with("Игрок")
    elif goose_type == "honk":
        mock_goose.honk.assert_called_once_with("Игрок")
    else:
        mock_goose.collab_attack.assert_called_once_with("Игрок")
    assert mock_player.hp == 80


def test_still_money(mocker, empty_casino, chip_100, capsys):
    player = Player("Игрок")
    player.balance = 100
    player.chips = [chip_100]

    mock_goose = mocker.Mock(spec=Goose)
    mock_goose.name = "Гусь"
    mock_goose.still_money.return_value = [chip_100]

    empty_casino.geese.append(mock_goose)
    empty_casino.players.append(player)

    simulate = Actions()
    simulate.still_money(empty_casino.geese, empty_casino.players)
    check_result = player_check(player)

    captured = capsys.readouterr()

    assert player.balance == 0
    assert player.chips == []
    assert player not in empty_casino.players
    assert check_result is False
    assert "🚔 Игрок забирает Гусе-полиция из-за неположительного счёта." in captured.out


def test_geese_collab(war_goose, honk_goose, empty_casino):
    simulate = Actions()
    geese = [war_goose, honk_goose]
    empty_casino.geese.extend(geese)
    flock = simulate.geese_collab(empty_casino.geese)

    assert isinstance(flock, GooseFlock)
    assert flock.size == 2
    assert war_goose in flock.geese and honk_goose in flock.geese
