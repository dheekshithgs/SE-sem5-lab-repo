import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


def test_wet_soil():
    assert should_irrigate(70, 0, "seedling") is False


def test_heavy_rain():
    assert should_irrigate(30, 12, "seedling") is False


def test_seedling_irrigation():
    assert should_irrigate(30, 0, "seedling") is True


def test_seedling_no_irrigation():
    assert should_irrigate(45, 0, "seedling") is False


def test_flowering_irrigation():
    assert should_irrigate(40, 0, "flowering") is True


def test_other_stage_rain():
    assert should_irrigate(30, 6, "vegetative") is False


def test_other_stage_irrigation():
    assert should_irrigate(30, 0, "vegetative") is True


def test_invalid_area():
    with pytest.raises(ValueError):
        water_volume(0, "seedling", 20)


def test_seedling_volume():
    assert water_volume(10, "seedling", 20) == 20


def test_flowering_volume():
    assert water_volume(10, "flowering", 20) == 50


def test_other_stage_volume():
    assert water_volume(10, "vegetative", 20) == 40


def test_high_temperature():
    assert water_volume(10, "seedling", 40) == 30


def test_low_temperature():
    assert water_volume(10, "seedling", 5) == 10


def test_schedule():
    zones = [
        ("Zone A", 10, 70, 0, "seedling", 20),
        ("Zone B", 10, 30, 0, "seedling", 20),
        ("Zone C", 10, 30, 0, "flowering", 20),
    ]
    assert schedule(zones, 25) == ["Zone B"]
