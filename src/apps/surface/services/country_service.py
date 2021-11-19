import logging
from typing import List
from src.apps.surface import models
from src.apps.surface.schemas import country_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("SurfaceCountryService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingCountry(Exception):
    pass


class FailedGettingCountry(Exception):
    pass


class FailedGettingCountryList(Exception):
    pass


class FailedUpdatingCountry(Exception):
    pass


class FailedDeletingCountry(Exception):
    pass


class CountryDoesNotExist(Exception):
    pass


def create(data: country_schema.CreateCountry) -> country_schema.Country:
    try:
        country = models.Country(**data.dict())
        country.save()
        return country_schema.Country.from_django(country)
    except Exception as e:
        logger.exception(e)
        raise FailedCreatingCountry("Failed creating country.")


def get(name: str) -> country_schema.Country:
    try:
        country = models.Country.objects.get(name=name)

        if not country:
            raise HTTPException(status_code=404, detail="Country does not exist.")

        return country_schema.Country.from_django(country)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingCountry("Failed getting country.")


def query(
        name: str = None,
        code: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[country_schema.Country]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `obselement` row skipping
    `offset` number of rows

    :param name: Full form of the name of the country
    :param code: Short form of name
    :param limit: describes page size
    :param offset: describe how many to skip
    :return: list of `obselement`
    """
    try:
        countries = models.Country.objects.all()

        if name is not None:
            countries.filter(name=name)

        if code is not None:
            countries.filter(code=code)

        return [country_schema.Country.from_django(c) for c in countries[offset:limit]]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingCountryList("Failed getting country list.")


def update(name: str, updates: country_schema.UpdateCountry) -> country_schema.Country:
    try:
        models.Country.objects.get(name=name).update(updates.dict())
        updated_country = models.Country.objects.get(name=name)
        return country_schema.Country.from_django(updated_country)
    except Exception as e:
        logger.exception(e)
        raise FailedUpdatingCountry("Failed updating country")


def delete(name: str) -> bool:
    try:
        models.Country.objects.get(name=name).delete()
        return True
    except Exception as e:
        logger.exception(e)
        raise FailedDeletingCountry("Failed deleting country.")




