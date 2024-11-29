from tcxparser import TCXParser
from datetime import datetime as dt
from datetime import timedelta as td
import logging
import json
from dateutil import parser
import pandas as pd


async def parse_csv_file(filename, file, logger):
    try:
        df = pd.read_csv(file)

        column_mapping = {
            "Aktivitätstyp": "activityType",
            "Datum": "date",
            "Favorit": "favorite",
            "Titel": "title",
            "Distanz": "distance",
            "Kalorien": "calories",
            "Zeit": "time",
            "Ø Herzfrequenz": "avgHeartRate",
            "Maximale Herzfrequenz": "maxHeartRate",
            "Aerober TE": "aerober_training_effect",
            "Ø Schrittfrequenz (Laufen)": "avg_cadence",
            "Max. Schrittfrequenz (Laufen)": "max_cadence",
            "Ø Pace": "avgPace",
            "Beste Pace": "max_pace",
            "Anstieg gesamt": "ascent",
            "Abstieg gesamt": "descent",
            "Ø Schrittlänge": "avg_stride_length",
            "Training Stress Score®": "tse",
            "Dekompression": "decompression",
            "Beste Rundenzeit": "best_lap_time",
            "Anzahl der Runden": "number_of_laps",
            "Zeit in Bewegung": "moving_time",
            "Verstrichene Zeit": "duration",
            "Minimale Höhe": "min_elevation",
            "Maximale Höhe": "max_elevation",
        }

        df.rename(columns=column_mapping, inplace=True)

        selected_columns = [
            "date",
            "duration",
            "distance",
            "activityType",
            "calories",
            "ascent",
            "avgPace",
            "maxHeartRate",
            "avgHeartRate",
        ]
        df_selected = df.loc[:, selected_columns]
        # Convert the DataFrame to a dictionary
        data = df_selected.to_dict(orient="records")

        for activity in data:
            activity["waypoints"] = []
            activity["minHeartRate"] = 0
            date = str(activity["date"]).split(" ")
            activity["fileName"] = "activity_" + date[0] + ".csv"
            activity["timeFinished"] = activity["date"]
            activity.pop("date", None)

        return data
    except Exception as e:
        logger.error(f"Error reading file: {repr(e)}")
        return {f"Exception: {repr(e)}"}
