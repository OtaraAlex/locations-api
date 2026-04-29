import json
import sys
from pathlib import Path

from sqlalchemy import delete

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.database import Base, SessionLocal, engine
from app.models import Location

DATA_FILE = BASE_DIR / "locations.json"


def build_search_document(item: dict) -> str:
    parts = [
        item.get("name"),
        item.get("category"),
        item.get("type"),
        item.get("county"),
        item.get("town"),
        item.get("address", {}).get("street"),
        item.get("address", {}).get("city"),
        item.get("address", {}).get("postcode"),
    ]
    return " ".join(part for part in parts if part)


def load_records() -> list[Location]:
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    records: list[Location] = []

    for collection_name in ("shopping_malls", "universities", "cafes", "supermarkets"):
        for item in payload.get(collection_name, []):
            address = item.get("address") or {}
            coordinates = item.get("coordinates") or {}
            records.append(
                Location(
                    source_collection=collection_name,
                    source_item_id=item["id"],
                    name=item["name"],
                    category=item["category"],
                    location_type=item.get("type"),
                    county=item.get("county"),
                    town=item.get("town"),
                    latitude=coordinates.get("lat"),
                    longitude=coordinates.get("lng"),
                    street=address.get("street"),
                    city=address.get("city"),
                    postcode=address.get("postcode"),
                    website=item.get("website"),
                    phone=item.get("phone"),
                    operator=item.get("operator"),
                    established=item.get("established"),
                    osm_tags=item.get("osm_tags"),
                    raw_payload=item,
                    search_document=build_search_document(item),
                )
            )
    return records


def main() -> None:
    records = load_records()
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.execute(delete(Location))
        db.add_all(records)
        db.commit()
    print(f"Seeded {len(records)} records from {DATA_FILE.name}.")


if __name__ == "__main__":
    main()
