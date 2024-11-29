from os import listdir
import os
import app.utility.handler_db as handler_db
from app.utility.logger_local import get_logger
from app.utility.parse_tcx_file import parse_tcx_file
import app.utility.queries_db as queries_db
import pytest

GLOBAL_LOGGER = get_logger()
GLOBAL_DATA_PARSED = []
GLOBAL_TABLE_NAME = "activities"
GLOBAL_DB_NAME = "testDB.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATH_TEST_DATA = os.path.join(BASE_DIR, "test_data")


async def mock_read_files():
    global GLOBAL_DATA_PARSED
    for file in listdir(PATH_TEST_DATA):
        if not handler_db.getRow(tableName=GLOBAL_TABLE_NAME, column="fileName", condition=file):
            data = await parse_tcx_file(
                filename=file, file=PATH_TEST_DATA + "/" + file, logger=GLOBAL_LOGGER
            )
            data.pop("waypoints", None)
            handler_db.addRow(GLOBAL_TABLE_NAME, data, GLOBAL_LOGGER)
            number_rows = handler_db.countRows(GLOBAL_TABLE_NAME, GLOBAL_LOGGER)
    GLOBAL_LOGGER.info(number_rows)
    return number_rows


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
    res = handler_db.get_table_names(GLOBAL_LOGGER)
    if res is not None:
        handler_db.dropTable(GLOBAL_TABLE_NAME, GLOBAL_LOGGER)


def test_check_creation_table():
    handler_db.checkConnection(GLOBAL_DB_NAME, GLOBAL_LOGGER)
    handler_db.createTable(GLOBAL_TABLE_NAME, queries_db.TABLE_ACITVITIES, GLOBAL_LOGGER)
    res = handler_db.get_table_names(GLOBAL_LOGGER)
    assert res[0][0] == "activities"


@pytest.mark.asyncio
async def test_read_files():
    handler_db.createTable(GLOBAL_TABLE_NAME, queries_db.TABLE_ACITVITIES, GLOBAL_LOGGER)
    res = await mock_read_files()
    assert res == 3


@pytest.mark.asyncio
async def test_get_avg():
    handler_db.createTable(GLOBAL_TABLE_NAME, queries_db.TABLE_ACITVITIES, GLOBAL_LOGGER)
    await mock_read_files()
    res = handler_db.getAvg(GLOBAL_TABLE_NAME, "distance", GLOBAL_LOGGER)
    assert round(float(res), 2) == 39.73


@pytest.mark.asyncio
async def test_get_total_time():
    handler_db.createTable(GLOBAL_TABLE_NAME, queries_db.TABLE_ACITVITIES, GLOBAL_LOGGER)
    await mock_read_files()
    res = handler_db.getTotalTime(GLOBAL_TABLE_NAME, GLOBAL_LOGGER)
    assert res == '5.0 "Hours", 51.0, "Minutes", 41.0, "Seconds"'


@pytest.mark.asyncio
async def test_get_sum():
    handler_db.createTable(GLOBAL_TABLE_NAME, queries_db.TABLE_ACITVITIES, GLOBAL_LOGGER)
    await mock_read_files()
    res = handler_db.getSum(GLOBAL_TABLE_NAME, "distance", GLOBAL_LOGGER)
    assert float(res) == 119.18
