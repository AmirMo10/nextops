"""Authorize existing administrators for the bounded Phase 2 Linux reader.

Revision ID: 0002_phase2_linux_read
Revises: 0001_durable_app
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_phase2_linux_read"
down_revision: str | None = "0001_durable_app"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Grant the explicit read-only Linux scope to existing administrators."""

    op.execute(
        sa.text(
            """
            UPDATE identities
            SET scopes = array_append(scopes, 'linux.read'),
                updated_at = now()
            WHERE 'admin' = ANY(roles)
              AND NOT ('linux.read' = ANY(scopes))
            """
        )
    )


def downgrade() -> None:
    """Remove only the Phase 2 Linux scope added by this migration."""

    op.execute(
        sa.text(
            """
            UPDATE identities
            SET scopes = array_remove(scopes, 'linux.read'),
                updated_at = now()
            WHERE 'admin' = ANY(roles)
            """
        )
    )
