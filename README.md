## Prava

This is a simple FastAPI backend that helps you to analyze your .tcx file, e.g. from [Garmin](https://connect.garmin.com/).\
For parsing the .tcx file, the [python-tcxparser](https://github.com/vkurup/python-tcxparser) Vinod Kurup is used.

## Setup

Create a Python environment and activate it.

1. `pip install -r requirements.txt`
2. `fastapi dev main.py`

Now you should be able to access the OpenAPI docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and call the API via [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage

All routes are defined within `app.py`.
Check out the [OpenAPI docs](http://127.0.0.1:8000/docs) for the respective endpoints.

**How can I upload a .tcx file and analyze it?**

On startup SQLlite `prava.db` and a table `activities` should be created.

Next, we want to upload a .tcx file:

```
POST /upload_files

Response:
{
  "message": "Successfully uploaded 3 files."
}
```

Afterward, we can parse and analyze the given file:

```
POST /process

Response:
{
  "total_distance": 134,
  "average_distance": 45,
  "avg_heart_rate": 139,
  "total_ascent": 1900,
  "total_time": "6.0 \"Hours\", 2.0, \"Minutes\", 51.0, \"Seconds\""
}
```

Basically, all data extracted by the [tcx-parser](https://github.com/vkurup/python-tcxparser) can be used for the analysis.\
Currently, the following helper functions are available in `utility/handler_db.py` for analyzing the data:

- getSum()
- getAvg()
- getTotalTime()

## Testing

For testing purposes there already some .tcx files existing within `tests/test_data`.\
For executing the tests:

1. `pip install -r requirements.txt`
2. `cd tests`
3. `pytest test_db.py`

## Running the API with Docker

You can create a docker container to use the API:

```sh
docker build -t prava-app .
docker run --name prava-app  -p 8080:8080 prava
```
