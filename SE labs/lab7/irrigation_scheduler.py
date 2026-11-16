def parse_zone(text):
    if not isinstance(text, str):
        return None

    try:
        name, area = text.split(':')
        name = name.strip()
        area = float(area)

        if not name or area < 0:
            return None

        return name.title(), area

    except (ValueError, TypeError):
        return None


def moisture_average(readings_csv):
    if not isinstance(readings_csv, str):
        return None

    try:
        values = [int(r.strip()) for r in readings_csv.split(',')]

        if not values:
            return None

        if any(v < 0 or v > 100 for v in values):
            return None

        return sum(values) // len(values)

    except (ValueError, TypeError):
        return None


def water_needed(text):
    if not isinstance(text, str):
        return None

    try:
        plot, rain = text.split('|')

        plot = float(plot)
        rain = float(rain)

        if plot < 0 or rain < 0:
            return None

        need = plot * 5 - rain
        return max(need, 0)

    except (ValueError, TypeError):
        return None


def main():
    print("==== Running parse_zone ====")
    user_input = input("Enter zone:area in m2 (e.g. north:120): ")
    result = parse_zone(user_input)
    print("Zone and Area:", result)

    print("\n==== Running moisture_average ====")
    user_input = input("Enter moisture readings as CSV (e.g. 40,35,50): ")
    result = moisture_average(user_input)
    print("Average Moisture:", result)

    print("\n==== Running water_needed ====")
    user_input = input("Enter area|rainfall (e.g. 120|8): ")
    result = water_needed(user_input)
    print("Water Needed:", result)


if __name__ == "__main__":
    main()