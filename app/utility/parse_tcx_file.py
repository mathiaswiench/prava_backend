from tcxparser import TCXParser
from datetime import datetime as dt
from datetime import timedelta as td
import logging
import json
from dateutil import parser


async def parse_tcx_file(filename, file, logger):
    try:
        tcx = TCXParser(file)
        zones = {
            "Z0": (0, 120),
            "Z1": (121, 140),
            "Z2": (141, 160),
            "Z3": (161, 240),
        }

        def safe_getattr(attr, default):
            value = getattr(tcx, attr, default)
            return default if value is None else value

        def safe_call(func, *args, default=None, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error calling function {func.__name__}: {repr(e)}")
                return default

        def parse_date(date: str):
            try:
                parsed_date = parser.isoparse(date)
                return parsed_date
            except ValueError as e:
                logger.error(f"Error reading file: {e}")
                logger.info({"Exception": str(e)})

        def convert_waypoints():
            waypoints_raw = safe_call(tcx.position_values, default=None)
            if waypoints_raw is None:
                logger.info("No waypoints found.")
                return {}
            converted_waypoints = []
            count = 0
            for waypoint in waypoints_raw:
                converted_waypoints.append(
                    {
                        "sequence": count,
                        "latitude": waypoint[0],
                        "longitude": waypoint[1],
                    }
                )
                count += 1

            return converted_waypoints

        data = {
            "fileName": filename,
            "duration": td(seconds=round(safe_getattr("duration", 0))).seconds,
            "distance": round(safe_getattr("distance", 0) / 1000, 2),
            "activityType": safe_getattr("activity_type", None),
            "calories": safe_getattr("calories", None),
            "ascent": round(safe_getattr("ascent", 0)),
            "avgPace": str(safe_getattr("pace", None)),
            "minHeartRate": int(safe_getattr("hr_min", 0)),
            "maxHeartRate": int(safe_getattr("hr_max", 0)),
            "avgHeartRate": int(safe_getattr("hr_avg", 0)),
            "timeFinished": str(parse_date(safe_getattr("completed_at", 0))),
            # "hr_time_zones": safe_call(tcx.hr_percent_in_zones, zones, default=None),
            "waypoints": convert_waypoints(),
        }
        return [data]
    except Exception as e:
        logger.error(f"Error reading file: {repr(e)}")
        return {f"Exception: {repr(e)}"}
