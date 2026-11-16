from hypothesis import given, strategies as st
from irrigation_scheduler import parse_zone, moisture_average, water_needed


# TEST 1: parse_zone

@given(st.text() | st.none())
def test_parse_zone_no_crash(s):
    result = parse_zone(s)
    assert result is None or (
        isinstance(result, tuple) and len(result) == 2
    )


@given(
    st.from_regex(r"[A-Za-z][A-Za-z0-9 _-]{0,19}", fullmatch=True),
    st.floats(min_value=0, max_value=10000,
              allow_nan=False, allow_infinity=False)
)
def test_parse_zone_valid(name, area):
    result = parse_zone(f"{name}:{area}")
    assert result == (name.strip().title(), area)


# TEST 2: moisture_average

@given(st.text() | st.none())
def test_moisture_average_no_crash(s):
    result = moisture_average(s)
    assert result is None or isinstance(result, int)


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1))
def test_moisture_average_valid(values):
    csv = ','.join(map(str, values))
    assert moisture_average(csv) == sum(values) // len(values)


# TEST 3: water_needed

@given(st.text() | st.none())
def test_water_needed_no_crash(s):
    result = water_needed(s)
    assert result is None or result >= 0


@given(
    st.floats(min_value=0, max_value=10000,
              allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=10000,
              allow_nan=False, allow_infinity=False)
)
def test_water_needed_valid(plot, rain):
    result = water_needed(f"{plot}|{rain}")
    assert result == max(plot * 5 - rain, 0)