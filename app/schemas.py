from pydantic import BaseModel, ConfigDict


class Coordinates(BaseModel):
    lat: float | None = None
    lng: float | None = None


class Address(BaseModel):
    street: str | None = None
    city: str | None = None
    postcode: str | None = None


class LocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_collection: str
    source_item_id: int
    name: str
    category: str
    location_type: str | None = None
    county: str | None = None
    town: str | None = None
    coordinates: Coordinates
    address: Address
    website: str | None = None
    phone: str | None = None
    operator: str | None = None
    established: int | None = None
    osm_tags: dict | None = None

    @classmethod
    def from_model(cls, location) -> "LocationRead":
        return cls(
            id=location.id,
            source_collection=location.source_collection,
            source_item_id=location.source_item_id,
            name=location.name,
            category=location.category,
            location_type=location.location_type,
            county=location.county,
            town=location.town,
            coordinates=Coordinates(lat=location.latitude, lng=location.longitude),
            address=Address(
                street=location.street,
                city=location.city,
                postcode=location.postcode,
            ),
            website=location.website,
            phone=location.phone,
            operator=location.operator,
            established=location.established,
            osm_tags=location.osm_tags,
        )


class LocationListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[LocationRead]


class FilterListResponse(BaseModel):
    total: int
    items: list[str]


class HealthResponse(BaseModel):
    status: str

