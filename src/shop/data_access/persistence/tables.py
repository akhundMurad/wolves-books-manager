from uuid import uuid4
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


metadata = sa.MetaData()


books = sa.Table(
    "books",
    metadata,
    sa.Column(
        "id", UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True
    ),
    sa.Column("title", sa.String(length=256), nullable=False),
    sa.Column("description", sa.Text, nullable=False),
    sa.Column(
        "author_full_name",
        sa.String(length=128),
        nullable=False,
    ),
    sa.Column("genre", sa.String(length=128), nullable=False),
    sa.Column("price", sa.Float, nullable=False),
    sa.Column("created_at", sa.DateTime, nullable=False),
)


ordered_books = sa.Table(
    "ordered_books",
    metadata,
    sa.Column("book_id", sa.ForeignKey("books.id")),
    sa.Column("order_id", sa.ForeignKey("orders.id")),
)


orders = sa.Table(
    "orders",
    metadata,
    sa.Column(
        "id", UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True
    ),
    sa.Column("customer", UUID(as_uuid=True)),
)
