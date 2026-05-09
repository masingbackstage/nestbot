"""add hnsw index on embedding

Revision ID: [nowa_rewizja]
Revises: 3c32b496086e
Create Date: 2026-05-08...

"""

from alembic import op

revision = "[nowa_rewizja]"
down_revision = "3c32b496086e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_memories_embedding_hnsw
        ON memories USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_memories_embedding_hnsw")
