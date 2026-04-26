from sqlalchemy import Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_collection: Mapped[str] = mapped_column(String(100), index=True)
    source_item_id: Mapped[int] = mapped_column(Integer, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    location_type: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    county: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    town: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    street: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    postcode: Mapped[str | None] = mapped_column(String(30), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(80), nullable=True)
    operator: Mapped[str | None] = mapped_column(String(255), nullable=True)
    established: Mapped[int | None] = mapped_column(Integer, nullable=True)
    osm_tags: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    raw_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    search_document: Mapped[str | None] = mapped_column(Text, nullable=True)

