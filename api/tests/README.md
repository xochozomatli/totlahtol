To conduct tests, go to the api folder and run (from the venv):

`python3 -m pytest`

for additional output:

`python3 -m pytest -v`

for even more output:

`python3 -m pytest -vv`

for test coverage:

`python3 -m pytest -v --cov=app`

normal pytest arguments work as well, placed before `--cov=app`.

See the docs for more information:

[pytest](https://pytest.org/en/latest/index.html)

[pytest-flask](https://pytest-flask.readthedocs.io)

[pytest-cov](https://pytest-flask.readthedocs.io)

