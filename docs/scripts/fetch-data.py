# %%
from subprocess import run
from sqlite_utils import Database
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from rich import progress, print

here = Path(__file__).parent
path_db = here / "../_static/github.db"

# %%
organizations = [
    "2i2c-org",
    "executablebooks",
    "jupyterhub",
    "jupyter",
]

# Fetch latest repositories
for org in progress.track(organizations):
    print(f"Fetching organization for {org}...")
    run(f"github-to-sqlite repos {path_db} {org}", shell=True)

# %%
# Grab a list of repositories that have been updated in the last year
# We'll only look at these to remove stale repositories
db = Database(path_db)
one_years_ago = datetime.today() - timedelta(days=365)
repositories = pd.DataFrame(db.query("SELECT * from repos"))
repositories = repositories.query(f"updated_at > '{one_years_ago:%Y-%m-%d}'")

# %%
# For each repository, fetch a bunch of metadata associated with it
kinds = [
    "issues",
    "pull-requests",
    "issue-comments",
]
for repo in progress.track(repositories["full_name"].values):
    for kind in kinds:
        print(f"Fetching {kind} from {repo}...")
        run(f"github-to-sqlite {kind} {path_db} {repo}", shell=True)
