from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import settings
from app.dependencies import get_db
from app.schemas import FilterListResponse, HealthResponse, LocationListResponse, LocationRead
from app.services import get_location, list_distinct_values, list_locations

router = APIRouter()


@router.get("/", summary="API overview")
def root() -> dict:
    return {
        "message": "Kenya Locations API for the book exchange app",
        "version": settings.app_version,
        "docs": "/docs",
        "endpoints": {
            "health": "GET /health",
            "locations": "GET /locations",
            "single_location": "GET /locations/{id}",
            "collections": "Filter with ?collection=shopping_malls or ?collection=universities",
            "search": "Filter with ?search=nairobi&county=Nairobi&town=Westlands",
            "filters": {
                "categories": "GET /filters/categories",
                "counties": "GET /filters/counties",
                "towns": "GET /filters/towns",
                "types": "GET /filters/types",
            },
        },
    }


@router.get("/health", response_model=HealthResponse, summary="Health check")
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/locations", response_model=LocationListResponse, summary="List locations")
def read_locations(
    collection: str | None = Query(default=None),
    category: str | None = Query(default=None),
    county: str | None = Query(default=None),
    town: str | None = Query(default=None),
    location_type: str | None = Query(default=None, alias="type"),
    search: str | None = Query(default=None, min_length=2),
    limit: int = Query(default=settings.default_page_size, ge=1, le=settings.max_page_size),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> LocationListResponse:
    total, items = list_locations(
        db,
        collection=collection,
        category=category,
        county=county,
        town=town,
        location_type=location_type,
        search=search,
        limit=limit,
        offset=offset,
    )
    return LocationListResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[LocationRead.from_model(item) for item in items],
    )


@router.get("/locations/{location_id}", response_model=LocationRead, summary="Get one location")
def read_location(location_id: int, db: Session = Depends(get_db)) -> LocationRead:
    item = get_location(db, location_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Location with ID {location_id} not found.")
    return LocationRead.from_model(item)


@router.get("/filters/categories", response_model=FilterListResponse, summary="List categories")
def read_categories(db: Session = Depends(get_db)) -> FilterListResponse:
    items = list_distinct_values(db, "category")
    return FilterListResponse(total=len(items), items=items)


@router.get("/filters/counties", response_model=FilterListResponse, summary="List counties")
def read_counties(db: Session = Depends(get_db)) -> FilterListResponse:
    items = list_distinct_values(db, "county")
    return FilterListResponse(total=len(items), items=items)


@router.get("/filters/towns", response_model=FilterListResponse, summary="List towns")
def read_towns(db: Session = Depends(get_db)) -> FilterListResponse:
    items = list_distinct_values(db, "town")
    return FilterListResponse(total=len(items), items=items)


@router.get("/filters/types", response_model=FilterListResponse, summary="List types")
def read_types(db: Session = Depends(get_db)) -> FilterListResponse:
    items = list_distinct_values(db, "location_type")
    return FilterListResponse(total=len(items), items=items)

