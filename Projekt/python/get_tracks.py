from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from mongoengine import Document, ObjectIdField, DateTimeField, FloatField
from config import mongoConfig
from tqdm import tqdm
from pprint import pprint


class Track(Document):
    vehicleId = ObjectIdField(required=True)
    ended = DateTimeField(required=True)
    distanceCalculated = FloatField(required=True)


class TrackRepository:
    def __init__(self,vehicle_id):
        self.vehicle_id = vehicle_id
        self.last_track = None
        self.last_day = None
        self.last_week = None
        self.last_month = None
        self.last_year = None
        self.start_date = None
        self.end_date = None
        self.distances_daily_dict = {}
        self.client = MongoClient(mongoConfig['host'],
                                  username=mongoConfig['username'],
                                  password=mongoConfig['password'],
                                  authSource=mongoConfig['authSource'],
                                  authMechanism=mongoConfig['authMechanism'])
        self.db = self.client['fleet']
        self.collection = self.db['track']


    def get_distance_for_static_frames(self, vehicle_id):
        timeframes = [1, 7, 30, 365]
        result = []

        for timeframe in timeframes:
            s = datetime.now()
            end_date = datetime(2023, 11, 6)
            start_date = end_date - timedelta(days=timeframe)

            pipeline = [
                {
                    "$match": {
                        "vehicleId": ObjectId(vehicle_id),
                        "ended": {"$gte": start_date, "$lt": end_date}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total_distance_calculated": {"$sum": "$distanceCalculated"}
                    }
                }
            ]

            data_aggregation_result = self.collection.aggregate(pipeline)

            total_distance_calculated = sum([item['total_distance_calculated'] for item in data_aggregation_result])

            result.append(total_distance_calculated / 1000)
            result = [round(num, 3) for num in result]
            print("%s - %s", timeframe, datetime.now() - s)

        self.last_day, self.last_week, self.last_month, self.last_year = result

        self.last_track = self.collection.find_one(
            {"vehicleId": ObjectId(vehicle_id)},
            projection={"distanceCalculated": True},
            sort=[("ended", -1)]
        )
        self.last_track = round(self.last_track["distanceCalculated"] / 1000, 3)

        result_tracks = [{
            "tracks": {
                "last_track_in_km": self.last_track,
                **{f"total_distance_in_{timeframes[i]}_days_in_km": result[i] for i in range(len(timeframes))}
            }
        }]

        return result_tracks

    def get_distance_for_timespan(self, start_date, end_date):

        pipeline = [
            {
                "$match": {
                    "vehicleId": ObjectId(self.vehicle_id),
                    "ended": {"$gte": start_date, "$lt": end_date}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_distance_calculated": {"$sum": "$distanceCalculated"}
                }
            }
        ]

        data_aggregation_result = self.collection.aggregate(pipeline)

        total_distance_calculated = [{"distance_for_timespan_in_km": round(
            sum([item['total_distance_calculated'] / 1000 for item in data_aggregation_result]), 3)}]

        return total_distance_calculated

    def get_daily_distances(self):
        current_year=datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime.now().replace(hour=0, minute=0)

        for _ in tqdm(range((end_date - start_date).days + 1), desc='Progress'):
            pipeline = [
                {
                    "$match": {
                        "vehicleId": ObjectId(self.vehicle_id),
                        "ended": {"$gte": start_date, "$lt": start_date + timedelta(days=1)}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total_distance_calculated": {"$sum": "$distanceCalculated"}
                    }
                }
            ]

            daily_value = list(self.collection.aggregate(pipeline))

            if len(daily_value) > 0 and daily_value[0]['total_distance_calculated'] != 0:
                dates= int(start_date.timestamp())
                distance=(float(round(daily_value[0]['total_distance_calculated'] / 1000)))
                self.distances_daily_dict[dates] = distance

            start_date += timedelta(days=1)

        pprint(self.distances_daily_dict)

        return self.distances_daily_dict


