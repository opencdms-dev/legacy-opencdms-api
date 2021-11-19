from faker import Faker


fake = Faker()


def get_valid_country_input():
    from src.apps.surface.schemas import country_schema
    return country_schema.CreateCountry(
        code=fake.country(),
        name=fake.country_code()
    )


