import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


def test_moisture_branches():
    assert should_irrigate(60, 0, "seedling") is False
    assert should_irrigate(59, 0, "seedling") is False


def test_rainfall_branches():
    assert should_irrigate(30, 10, "seedling") is False
    assert should_irrigate(30, 9, "seedling") is True


def test_seedling_branches():
    assert should_irrigate(44, 0, "seedling") is True
    assert should_irrigate(45, 0, "seedling") is False


def test_flowering_branches():
    assert should_irrigate(54, 0, "flowering") is True
    assert should_irrigate(55, 0, "flowering") is False


def test_other_stage_rain_branches():
    assert should_irrigate(30, 5, "vegetative") is False
    assert should_irrigate(30, 4, "vegetative") is True


def test_other_stage_moisture_branches():
    assert should_irrigate(39, 0, "vegetative") is True
    assert should_irrigate(40, 0, "vegetative") is False


def test_area_validation_branches():
    with pytest.raises(ValueError):
        water_volume(0, "seedling", 20)
    with pytest.raises(ValueError):
        water_volume(-5, "seedling", 20)
    assert water_volume(10, "seedling", 20) == 20


def test_growth_stage_branches():
    assert water_volume(10, "seedling", 20) == 20
    assert water_volume(10, "flowering", 20) == 50
    assert water_volume(10, "vegetative", 20) == 40


def test_temperature_branches():
    assert water_volume(10, "seedling", 36) == 30
    assert water_volume(10, "seedling", 35) == 20
    assert water_volume(10, "seedling", 9) == 10
    assert water_volume(10, "seedling", 10) == 20


def test_empty_schedule():
    assert schedule([], 100) == []


def test_skip_zone():
    zones = [("Zone A", 10, 70, 0, "seedling", 20)]
    assert schedule(zones, 100) == []


def test_successful_schedule():
    zones = [
        ("Zone A", 10, 30, 0, "seedling", 20),
        ("Zone B", 10, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 100) == ["Zone A", "Zone B"]


def test_insufficient_budget():
    zones = [("Zone A", 10, 30, 0, "seedling", 20)]
    assert schedule(zones, 10) == []


def test_budget_exhaustion():
    zones = [
        ("Zone A", 10, 30, 0, "seedling", 20),
        ("Zone B", 10, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 20) == ["Zone A"]
