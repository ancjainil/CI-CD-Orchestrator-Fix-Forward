"""initial tables"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "installations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("github_installation_id", sa.Integer(), unique=True, index=True),
        sa.Column("account_login", sa.String(length=255)),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        "repos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(length=255), unique=True, index=True),
        sa.Column("installation_id", sa.Integer(), sa.ForeignKey("installations.id")),
        sa.Column("default_branch", sa.String(length=255), server_default="main"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "pull_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("repo_id", sa.Integer(), sa.ForeignKey("repos.id")),
        sa.Column("number", sa.Integer()),
        sa.Column("head_sha", sa.String(length=64)),
        sa.Column("base_sha", sa.String(length=64)),
        sa.Column("title", sa.String(length=512)),
        sa.Column("author", sa.String(length=255)),
        sa.Column("status", sa.String(length=255), server_default="open"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        "workflow_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("repo_id", sa.Integer(), sa.ForeignKey("repos.id"), nullable=True),
        sa.Column("pr_id", sa.Integer(), sa.ForeignKey("pull_requests.id"), nullable=True),
        sa.Column("status", sa.String(length=255), server_default="pending"),
        sa.Column("conclusion", sa.String(length=255), nullable=True),
        sa.Column("raw", sa.JSON(), server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "check_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("workflow_run_id", sa.Integer(), sa.ForeignKey("workflow_runs.id")),
        sa.Column("name", sa.String(length=255)),
        sa.Column("status", sa.String(length=255), server_default="queued"),
        sa.Column("conclusion", sa.String(length=255), nullable=True),
        sa.Column("log_excerpt", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pr_id", sa.Integer(), sa.ForeignKey("pull_requests.id")),
        sa.Column("status", sa.String(length=255), server_default="pending"),
        sa.Column("started_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("result_json", sa.JSON(), server_default=sa.text("'{}'::jsonb")),
        sa.Column("trace", sa.Text(), nullable=True),
    )
    op.create_table(
        "slo_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("service", sa.String(length=255)),
        sa.Column("window", sa.String(length=64)),
        sa.Column("latency_p95", sa.Float()),
        sa.Column("error_rate", sa.Float()),
        sa.Column("burn_rate", sa.Float()),
        sa.Column("budget_remaining", sa.Float()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "fix_forward_patches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("agent_run_id", sa.Integer(), sa.ForeignKey("agent_runs.id")),
        sa.Column("branch", sa.String(length=255)),
        sa.Column("pr_url", sa.String(length=512)),
        sa.Column("diff_summary", sa.Text()),
        sa.Column("risk_score", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("fix_forward_patches")
    op.drop_table("slo_snapshots")
    op.drop_table("agent_runs")
    op.drop_table("check_runs")
    op.drop_table("workflow_runs")
    op.drop_table("pull_requests")
    op.drop_table("repos")
    op.drop_table("installations")
