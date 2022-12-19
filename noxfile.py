import nox
import os

nox.options.reuse_existing_virtualenvs = True

@nox.session
def lab(session):
    session.install("-r", "requirements.txt")
    session.run(*"jupyter lab".split(), env={"GITHUB_ACCESS_TOKEN": os.environ.get("GITHUB_TOKEN")})
