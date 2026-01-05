# little form

A little server to handle forms submission.

## Features

- Configure your forms
- Get notified when a form is submitted

## Run it
```sh
docker build . -t little_form
docker run -p 8000:8000 little_form
```

## Development

- Install deps: `uv sync --all-extras`
- Run it:
```sh
export FLASK_APP=app
cd little_form
uv run flask db upgrade
uv run flask run
```
- Run tests: `uv run pytest`
- Lint and format: `pre-commit run --all-files`
- Before commit: `pre-commit install`

## License

This project is licensed under the Apache-2.0. See [LICENSE](LICENSE) for details.


**Made with ❤️**