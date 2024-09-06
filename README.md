## Prava

This is a simple FastAPI backend that helps you to analyze your .tcx file, e.g. from [Garmin](https://connect.garmin.com/).\
For parsing the .tcx file, the [python-tcxparser](https://github.com/vkurup/python-tcxparser) Vinod Kurup is used.

## Setup
Create a Python environment and activate it.

1. `pip install -r requirements.txt`
2. `fastapi dev app.py`

Now you should be able to access the OpenAPI docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and call the API via [http://127.0.0.1:8000](http://127.0.0.1:8000)
