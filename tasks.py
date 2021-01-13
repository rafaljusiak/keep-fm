from invoke import task

DOCKER = "docker-compose"
DOCKER_RUN = f"{DOCKER} run --rm django"


def docker(c, command, **kwargs):
    c.run(f"{DOCKER} {command}", **kwargs)


def docker_run(c, command, **kwargs):
    c.run(f"{DOCKER_RUN} {command}", **kwargs)


@task
def build(c):
    docker(c, "build")


@task
def start(c):
    docker(c, "up -d")


@task
def stop(c):
    docker(c, "stop")


@task
def makemigrations(c, args=""):
    docker_run(c, f"python manage.py makemigrations {args}")


@task
def pytest(c, args=""):
    docker_run(c, f"pytest . {args}")


@task
def migrate(c):
    docker_run(c, "python manage.py migrate")


@task
def collectstatic(c):
    docker_run(c, "python manage.py collectstatic --noinput")


@task
def shell(c):
    docker_run(c, "sh", pty=True)


@task
def python_shell(c):
    docker_run(c, "python manage.py shell", pty=True)


@task
def create_super_user(c):
    docker_run(c, "python manage.py createsuperuser", pty=True)


@task
def update_data(c, usernames):
    docker_run(c, f"python manage.py scrobbles {usernames}")


@task
def quality(c):
    docker_run(c, "black .")
    docker_run(c, "flake8 .")
    docker_run(c, "mypy")


@task
def quality_check(c):
    docker_run(c, "black . --check")
    docker_run(c, "flake8 .")
    docker_run(c, "mypy")


@task
def bandit(c):
    docker_run(c, "bandit -r .")


@task
def add_dep(c, dependency):
    docker_run(c, "poetry add " + dependency)


@task
def add_dev_dep(c, dependency):
    docker_run(c, "poetry add -D " + dependency)


@task
def update_dep(c, dependencies):
    docker_run(c, "poetry update " + dependencies)


@task
def install_deps(c):
    docker_run(c, "poetry install --no-interaction --no-ansi -vvv")


@task
def initial_setup(c):
    c.run("touch .env.local")
    build(c)
    migrate(c)
    collectstatic()
    create_super_user(c)
