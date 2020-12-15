from invoke import task


@task
def clean_pyc(c):
    """
    Remove python file artifacts
    """
    c.run("find . -name '*.pyc' -exec rm -f {} +")
    c.run("find . -name '*.pyo' -exec rm -f {} +")
    c.run("find . -name '*~' -exec rm -f {} +")


@task
def coverage(c):
    """
    check code coverage quickly with the default Python
    """
    c.run("cd testapp/app && coverage run --source admin_export_action manage.py test")
    c.run("cd testapp/app && coverage report -m")
    c.run("cd testapp/app && coverage html")
    c.run("cd testapp/app && xdg-open htmlcov/index.html")


@task
def unittest(c):
    """
    Run unittests, run the command inside the testapp/app directory
    """
    c.run("cd testapp/app && python manage.py test")
