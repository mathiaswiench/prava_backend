from typing import List, Optional
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel

from app.baml_client.types import Activity
from app.utility.parse_csv_file import parse_csv_file
from .utility import handler_db, queries_db
from .utility.logger_local import get_logger
from .utility.parse_tcx_file import parse_tcx_file
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from fastapi.responses import HTMLResponse
import logging
from .baml_client.sync_client import b
import os
from baml_py import ClientRegistry
from dotenv import load_dotenv
import pandas as pd


GLOBAL_LOGGER = None
GLOBAL_TABLE_ACTIVITIES = "activities"
GLOBAL_TABLE_WAYPOINTS = "waypoints"
GLOBAL_DB_NAME = "prava.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DATA = os.path.join(BASE_DIR, "data")
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global GLOBAL_LOGGER
    GLOBAL_LOGGER = get_logger()
    if not os.path.isdir(PATH_DATA):
        os.makedirs(PATH_DATA)
    handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
    if not handler_db.get_table_names(GLOBAL_LOGGER):
        try:
            handler_db.createTable(
                GLOBAL_TABLE_ACTIVITIES, queries_db.TABLE_ACITVITIES, GLOBAL_LOGGER
            )
            handler_db.createTable(
                GLOBAL_TABLE_WAYPOINTS, queries_db.TABLE_WAYPOINTS, GLOBAL_LOGGER
            )
            res = handler_db.get_table_names(GLOBAL_LOGGER)
            GLOBAL_LOGGER.info(f"Successfully created table: {res[0]}")
        except Exception as e:
            GLOBAL_LOGGER.error(f"Error creating the DB: {e}")
    GLOBAL_LOGGER.info("API is starting up")

    # Create baml client
    cr = ClientRegistry()
    token = os.environ.get("OPENAI_API_KEY")
    cr.add_llm_client(
        name="CustomGPT4o",
        provider="openai",
        options={"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")},
    )
    cr.set_primary("CustomGPT4o")

    yield


def create_app():

    app = FastAPI(lifespan=lifespan, root_path="", docs_url="/docs")

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/ping")
    async def ping():
        return {"message": "Up and running"}

    @app.get("/get_activities")
    async def get_activities(with_waypoints: Optional[bool] = False) -> List[Activity] | None:
        try:
            activities = handler_db.getActivities(
                tableName=GLOBAL_TABLE_ACTIVITIES,
                logger=GLOBAL_LOGGER,
                with_waypoints=with_waypoints,
            )
            return activities
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching all activities: {e}")

    @app.post("/upload_files")
    async def upload_files(files: list[UploadFile]):
        # TODO
        # Check if the file is a .tcx file
        uploaded_files = []
        try:
            # Upload files
            for file in files:
                if ".tcx" in file.filename:
                    with open(PATH_DATA + file.filename, "wb") as f:
                        while contents := file.file.read(1024 * 1024):
                            f.write(contents)
                    uploaded_files.append(file.filename)
                    file.file.close()
                elif ".csv" in file.filename:
                    with open(PATH_DATA + file.filename, "wb") as f:
                        content = file.file.read()
                        f.write(content)
                    uploaded_files.append(file.filename)
                    file.file.close()
                else:
                    continue
            # Parse Files
            await parse_files()
        except Exception as e:
            return {f"message": "There was an error uploading the file: {repr(e)}"}

        return {"message": f"Successfully uploaded {len(uploaded_files)} files."}

    @app.post("/parse_files")
    async def parse_files():
        files_parsed = []
        GLOBAL_LOGGER.info(PATH_DATA)
        for file in os.listdir(PATH_DATA):
            if not handler_db.getRow(
                tableName=GLOBAL_TABLE_ACTIVITIES, column="fileName", condition=file
            ):
                if ".csv" in file:
                    data = await parse_csv_file(
                        filename=file, file=PATH_DATA + "/" + file, logger=GLOBAL_LOGGER
                    )
                if ".tcx" in file:
                    data = await parse_tcx_file(
                        filename=file, file=PATH_DATA + "/" + file, logger=GLOBAL_LOGGER
                    )
                for d in data:
                    files_parsed.append(d["fileName"])
                    only_waypoints = d["waypoints"]
                    d.pop("waypoints", None)
                    handler_db.addRow(GLOBAL_TABLE_ACTIVITIES, d, GLOBAL_LOGGER)
                    row = handler_db.getRow(
                        tableName=GLOBAL_TABLE_ACTIVITIES,
                        column="fileName",
                        condition=d["fileName"],
                    )
                    if row is not None and len(only_waypoints) > 0:
                        for entry in only_waypoints:
                            data = {
                                "sequence": entry["sequence"],
                                "longitude": entry["longitude"],
                                "latitude": entry["latitude"],
                                "waypointFile": row[0],
                            }
                            handler_db.addRow(GLOBAL_TABLE_WAYPOINTS, data, GLOBAL_LOGGER)

        return {
            "message": f"Successfully parsed {len(files_parsed)} files: {files_parsed}",
            "data": len(files_parsed),
        }

    @app.post("/analyze_activities")
    def analyze_activities():
        try:
            handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
            distance = round(handler_db.getSum(GLOBAL_TABLE_ACTIVITIES, "distance", GLOBAL_LOGGER))
            average_distance = round(
                handler_db.getAvg(GLOBAL_TABLE_ACTIVITIES, "distance", GLOBAL_LOGGER)
            )
            avg_heart_rate = round(
                handler_db.getAvg(GLOBAL_TABLE_ACTIVITIES, "avgHeartRate", GLOBAL_LOGGER)
            )
            total_ascent = round(
                handler_db.getSum(GLOBAL_TABLE_ACTIVITIES, "ascent", GLOBAL_LOGGER)
            )
            total_time = handler_db.getTotalTime(GLOBAL_TABLE_ACTIVITIES, GLOBAL_LOGGER)

            data = {
                "total_distance": distance,
                "average_distance": average_distance,
                "avg_heart_rate": avg_heart_rate,
                "total_ascent": total_ascent,
                "total_time": total_time,
            }
            return data
        except Exception as e:
            return {f"Error: {e}"}

    @app.post("/create_table")
    async def create_table():
        try:
            handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
            handler_db.createTable(
                GLOBAL_TABLE_ACTIVITIES, queries_db.TABLE_ACITVITIES, GLOBAL_LOGGER
            )
            handler_db.createTable(
                GLOBAL_TABLE_WAYPOINTS, queries_db.TABLE_WAYPOINTS, GLOBAL_LOGGER
            )
            res = handler_db.get_table_names(GLOBAL_LOGGER)
            return {"message": f"Successfully created table: {res}"}
        except Exception as e:
            return {"message": f"Error creating the DB: {e}"}

    @app.post("/drop_table")
    async def drop_table():
        try:
            handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
            res1 = handler_db.dropTable(GLOBAL_TABLE_ACTIVITIES, GLOBAL_LOGGER)
            res2 = handler_db.dropTable(GLOBAL_TABLE_WAYPOINTS, GLOBAL_LOGGER)
            return {"message": f"Deleted table {res1, res2}"}
        except Exception as e:
            return {"message": f"{e}"}

    @app.post("/baml")
    async def baml():
        data: List[Activity] | None = await get_activities()

        if data is not None:
            response = b.TrainingPlanGenerator(data)
            logging.info(response)
            return response

    return app


def main():
    uvicorn.run(
        "app.main:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
