# TABLE_ACTIVITIES = [
#     ("fileName", "string"),
#     ("duration", "float"),
#     ("distance", "float"),
#     ("activityType", "string"),
#     ("calories", "int"),
#     ("ascent", "int"),
#     ("avgPace", "string"),
#     ("minHeartRate", "int"),
#     ("maxHeartRate", "int"),
#     ("avgHeartRate", "int"),
#     ("timeFinished", "string"),
# ]

TABLE_ACITVITIES = """
CREATE TABLE activities (
    fileId    INTEGER PRIMARY KEY,  
    fileName STRING,
    duration FLOAT,
    distance FLOAT,
    activityType STRING,
    calories INT,
    ascent INT,
    avgPace INT,
    minHeartRate INT,
    maxHeartRate INT,
    avgHeartRate INT,
    timeFinished STRING
);
"""

TABLE_WAYPOINTS = """
CREATE TABLE waypoints (
    latitude FLOAT,
    longitude FLOAT,
    sequence INT,
    waypointFile INT,
    FOREIGN KEY(waypointFile) REFERENCES activities(fileId)
);
"""
