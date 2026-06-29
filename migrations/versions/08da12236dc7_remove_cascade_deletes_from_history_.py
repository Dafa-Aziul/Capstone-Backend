"""remove cascade deletes from history relations

Revision ID: 08da12236dc7
Revises: 
Create Date: 2026-06-29 15:04:13.435811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "08da12236dc7"
down_revision = None
branch_labels = None
depends_on = None


def _replace_fk(table_name, constrained_column, referred_table, referred_column, ondelete):
    bind = op.get_bind()
    inspector = inspect(bind)
    foreign_keys = inspector.get_foreign_keys(table_name)

    target_fk = next(
        (
            fk
            for fk in foreign_keys
            if fk.get("constrained_columns") == [constrained_column]
            and fk.get("referred_table") == referred_table
            and fk.get("referred_columns") == [referred_column]
        ),
        None,
    )

    constraint_name = (
        target_fk.get("name")
        if target_fk and target_fk.get("name")
        else f"fk_{table_name}_{constrained_column}_{referred_table}"
    )

    if target_fk and target_fk.get("name"):
        op.drop_constraint(target_fk["name"], table_name, type_="foreignkey")

    op.create_foreign_key(
        constraint_name,
        table_name,
        referred_table,
        [constrained_column],
        [referred_column],
        onupdate="CASCADE",
        ondelete=ondelete,
    )


def upgrade():
    _replace_fk("ml_models", "uploaded_by", "users", "id_user", None)
    _replace_fk("riwayat_prediksi", "id_user", "users", "id_user", None)
    _replace_fk("riwayat_prediksi", "id_model", "model_kendaraan", "id_model", None)
    _replace_fk("riwayat_prediksi", "id_ml_model", "ml_models", "id_ml_model", None)
    _replace_fk("model_kendaraan", "id_merek", "merek", "id_merek", None)


def downgrade():
    _replace_fk("ml_models", "uploaded_by", "users", "id_user", "CASCADE")
    _replace_fk("riwayat_prediksi", "id_user", "users", "id_user", "CASCADE")
    _replace_fk("riwayat_prediksi", "id_model", "model_kendaraan", "id_model", "CASCADE")
    _replace_fk("riwayat_prediksi", "id_ml_model", "ml_models", "id_ml_model", "CASCADE")
    _replace_fk("model_kendaraan", "id_merek", "merek", "id_merek", "CASCADE")
