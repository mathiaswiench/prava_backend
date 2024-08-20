from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import utility.handler_db as handler_db
from utility.logger_local import get_logger
from utility.read_file import read_file
import utility.types_db as types_db
from pathlib import Path
from os import listdir



app = FastAPI()

GLOBAL_LOGGER = None
GLOBAL_DATA_PARSED = []
GLOBAL_TABLE_NAME = "activities"
GLOBAL_DB_NAME = "prava.db"

PATH_DATA = 'data/'

@app.on_event("startup")
async def startup_event():
    global GLOBAL_LOGGER
    GLOBAL_LOGGER = get_logger()
    GLOBAL_LOGGER.info('API is starting up')

@app.post("/create_table")
def create_table():
    try: 
        handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
        # handler_db.dropTable(GLOBAL_TABLE_NAME, GLOBAL_LOGGER)
        handler_db.createTable(GLOBAL_TABLE_NAME, types_db.DB_SCHEMA, GLOBAL_LOGGER)    
        res = handler_db.get_table_names(GLOBAL_LOGGER)
        return {"message": f"Successfully created table: {res[0]}"}
    except Exception as e:
        return {"message": f"Error creating the DB: {e}"}

@app.post("/readFiles")
async def read_files():
    global GLOBAL_DATA_PARSED
    for file in listdir(PATH_DATA):
        if not handler_db.check_activitiy_exists(GLOBAL_TABLE_NAME, file, GLOBAL_LOGGER):
            data = await read_file(filename=file, file=PATH_DATA+file, logger=GLOBAL_LOGGER)
            GLOBAL_DATA_PARSED.append(data)
            handler_db.addRow(GLOBAL_TABLE_NAME, data, GLOBAL_LOGGER)
            number_rows = handler_db.countRows(GLOBAL_TABLE_NAME, GLOBAL_LOGGER)
    return {"message": f"Successfully parsed {number_rows} files."}


@app.post("/upload")
async def upload_file(files: list[UploadFile]):
    #TODO
    #Check if the file is a .tcx file
    uploaded_files = []
    try:
        for file in files:
            if ".tcx" in file.filename:
                with open(PATH_DATA+file.filename, 'wb') as f:
                    while contents := file.file.read(1024 * 1024):
                        f.write(contents)
                uploaded_files.append(file.filename)
                file.file.close()
            else:
                continue
    except Exception as e:
        return {f'message": "There was an error uploading the file: {repr(e)}'}
        
    return {"message": f"Successfully uploaded {len(uploaded_files)} files."}

@app.post("/analyze")
def analyze():
    try:
        handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
        distance = round(handler_db.getSum(GLOBAL_TABLE_NAME, 'distance', GLOBAL_LOGGER))
        average_distance = round(handler_db.getAvg(GLOBAL_TABLE_NAME, 'distance', GLOBAL_LOGGER))
        avg_heart_rate = round(handler_db.getAvg(GLOBAL_TABLE_NAME, 'avgHeartRate', GLOBAL_LOGGER))
        total_ascent = round(handler_db.getSum(GLOBAL_TABLE_NAME, 'ascent', GLOBAL_LOGGER))
        total_time = handler_db.getTotalTime(GLOBAL_TABLE_NAME, GLOBAL_LOGGER)
        return {
            'total_distance': distance,
            'average_distance': average_distance,
            'avg_heart_rate': avg_heart_rate,
            'total_ascent': total_ascent,
            'total_time': total_time
        }
    except Exception as e:
        return {f'Error: {e}'}
    
@app.post("/drop_table")
async def drop_table():
    try:
        handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
        handler_db.dropTable(GLOBAL_TABLE_NAME, GLOBAL_LOGGER)
        return {"message": f"Deleted table {GLOBAL_TABLE_NAME}"}
    except Exception as e:
        return {"message": f"{e}"}
    
