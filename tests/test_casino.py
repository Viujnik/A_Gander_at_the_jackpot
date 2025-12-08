from src.models.characters import HonkGoose, Player


def test_player_register(mocker, empty_casino, chip_100, capsys):
    mocker.patch("random.choice", side_effect=["Игрок", 100])
    mocker.patch("random.randint", return_value=100)

    player = empty_casino.player_register()
    player_chips = [c.value for c in player.chips]
    captured = capsys.readouterr()

    assert isinstance(player, Player)
    assert "👤 Зарегистрирован: Игрок" in captured.out
    assert player in empty_casino.players
    assert player.balance == 100
    assert player_chips == [100]


def test_goose_register(mocker, empty_casino, capsys):
    mocker.patch("random.choice", return_value="Крикун")
    mocker.patch("random.randint", side_effect=[3, 5])
    goose = empty_casino.goose_register("honk")
    captured = capsys.readouterr()

    assert isinstance(goose, HonkGoose)
    assert "📢 Зарегистрирован крикливый гусь: Крикун; Наглость: 3)" in captured.out
    assert goose in empty_casino.geese
