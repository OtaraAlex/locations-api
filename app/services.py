from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Location


def apply_location_filters(
    stmt: Select,
    *,
    collection: str | None = None,
    category: str | None = None,
    county: str | None = None,
    town: str | None = None,
    location_type: str | None = None,
    search: str | None = None,
) -> Select:
    if collection:
        stmt = stmt.where(Location.source_collection.ilike(collection))
    if category:
        stmt = stmt.where(Location.category.ilike(category))
    if county:
        stmt = stmt.where(Location.county.ilike(county))
    if town:
        stmt = stmt.where(Location.town.ilike(town))
    if location_type:
        stmt = stmt.where(Location.location_type.ilike(location_type))
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                Location.name.ilike(pattern),
                Location.county.ilike(pattern),
                Location.town.ilike(pattern),
                Location.city.ilike(pattern),
                Location.street.ilike(pattern),
                Location.search_document.ilike(pattern),
            )
        )
    return stmt


def list_locations(
    db: Session,
    *,
    collection: str | None = None,
    category: str | None = None,
    county: str | None = None,
    town: str | None = None,
    location_type: str | None = None,
    search: str | None = None,
    limit: int = settings.default_page_size,
    offset: int = 0,
) -> tuple[int, list[Location]]:
    base_stmt = apply_location_filters(
        select(Location),
        collection=collection,
        category=category,
        county=county,
        town=town,
        location_type=location_type,
        search=search,
    )

    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = db.scalar(count_stmt) or 0

    items_stmt = (
        base_stmt.order_by(Location.name.asc())
        .offset(offset)
        .limit(min(limit, settings.max_page_size))
    )
    items = list(db.scalars(items_stmt).all())
    return total, items


def get_location(db: Session, location_id: int) -> Location | None:
    return db.get(Location, location_id)


def list_distinct_values(db: Session, field_name: str) -> list[str]:
    field = getattr(Location, field_name)
    stmt = (
        select(field)
        .where(field.is_not(None))
        .distinct()
        .order_by(field.asc())
    )
    return [value for value in db.scalars(stmt).all() if value]

