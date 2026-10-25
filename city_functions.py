def city_country(city, country, population=None, language=None):
    result = f"{city}, {country}"
    if population is not None:
        result += f" - population {population}"
    if language is not None:
        result += f", {language}"
    return result


if __name__ == "__main__":
    print(city_country("Santiago", "Chile"))
    print(city_country("Tokyo", "Japan", 13960000))
    print(city_country("Lima", "Peru", 9674755, "Spanish"))
