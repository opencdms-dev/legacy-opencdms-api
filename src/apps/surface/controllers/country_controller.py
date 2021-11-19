from fastapi import APIRouter, Depends
from src.apps.surface.services import country_service
from src.apps.surface.schemas import country_schema
from src.utils.response import get_success_response, get_error_response


router = APIRouter(
    prefix="/api/v1/surface",
    tags=["surface"]
)


@router.get("/countries", response_model=country_schema.CountryResponse)
def get_countries(
        name: str = None,
        code: str = None,
        limit: int = 25,
        offset: int = 0
):
    try:
        countries = country_service.query(
            name=name,
            code=code,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=countries, message="Successfully fetched countries.")
    except country_service.FailedGettingCountryList as e:
        return get_error_response(message=str(e))


@router.get("/countries/{name}", response_model=country_schema.CountryResponse)
def get_country_by_id(name: str):
    try:
        return get_success_response(
            result=[country_service.get(name=name)],
            message="Successfully fetched country."
        )
    except country_service.FailedGettingCountry as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/countries", response_model=country_schema.CountryResponse)
def create_country(data: country_schema.CreateCountry):
    try:
        return get_success_response(
            result=[country_service.create(data=data)],
            message="Successfully created country."
        )
    except country_service.FailedCreatingCountry as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/countries/{name}", response_model=country_schema.CountryResponse)
def update_country(name: str, data: country_schema.UpdateCountry):
    try:
        return get_success_response(
            result=[country_service.update(name=name, updates=data)],
            message="Successfully updated country."
        )
    except country_service.FailedUpdatingCountry as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/countries/{name}", response_model=country_schema.CountryResponse)
def delete_country(name: str):
    try:
        country_service.delete(name=name)
        return get_success_response(
            result=[],
            message="Successfully deleted country."
        )
    except country_service.FailedDeletingCountry as e:
        return get_error_response(
            message=str(e)
        )





