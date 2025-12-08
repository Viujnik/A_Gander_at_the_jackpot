import pytest
import random
from src.models.characters import Player, Chip, WarGoose, HonkGoose
from src.models.collections_models import PlayerCollection, ChipCollection
from src.models.casino import Casino


@pytest.fixture(autouse=True)
def set_random_seed():
    """Устанавливает seed=5 перед тестами."""
    random.seed(5)
    yield
    random.seed()


@pytest.fixture
def test_player():
    """Создаёт тестового игрока для тестов с фиксированными именем и фишками."""
    player = Player("Тестовый Игрок")
    player.chips = [Chip(100), Chip(50), Chip(25), Chip(10)]
    player.balance = 185
    return player


@pytest.fixture
def war_goose():
    """Создаёт военного гуся с фиксированно audacity."""
    goose = WarGoose("Тестовый Воин")
    goose.audacity = 5
    return goose


@pytest.fixture
def honk_goose():
    """Создаёт крикливого гуся с фиксированной audacity."""
    goose = HonkGoose("Тестовый Крикун")
    goose.audacity = 3
    return goose


@pytest.fixture
def empty_casino():
    """Создаёт пустое казино для тестов."""
    casino = Casino()
    casino.players = PlayerCollection()
    casino.geese = []
    casino.chips_balance = ChipCollection()
    return casino


@pytest.fixture
def chip_100():
    """Фишка на 100 ганс"""
    return Chip(100)


@pytest.fixture
def chip_50():
    """Фишка на 50 ганс"""
    return Chip(50)


@pytest.fixture
def mock_random_choice(mocker):
    """Подменяет random.choice, чтобы возвращать первое значение и контролировать случайный выбор в тестах."""

    def mock_choice(items):
        return items[0] if items else None

    mocker.patch("random.choice", side_effect=mock_choice)
