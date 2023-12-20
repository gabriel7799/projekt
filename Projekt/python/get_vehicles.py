from bson import ObjectId
from pymongo import MongoClient
from config import mongoConfig
from mongoengine import Document, ObjectIdField, StringField,FloatField


class Vehicle(Document):
    _id = ObjectIdField(required=True)
    type = StringField(required=False)
    model = StringField(required=False)
    brand = StringField(required=False)
    organisation = StringField(required=True)
    licensePlate=StringField(required=True)
    trackedDistance=FloatField(required=False)
    urbanPercentage=FloatField(required=False)
    highwayPercentage = FloatField(required=False)


class VehicleRepository:
    def __init__(self):
        self.client = MongoClient(mongoConfig['host'],
                                  username=mongoConfig['username'],
                                  password=mongoConfig['password'],
                                  authSource=mongoConfig['authSource'],
                                  authMechanism=mongoConfig['authMechanism'])


        self.db = self.client['fleet']
        self.collection = self.db['vehicle']

    def list_licenseplate_for_organisation(self, organisation_id):
        # Hier wird nach der organisation_id gesucht und die dazugehörigen License Plates zurückgegeben
        list_plates = list(
            self.collection.find(
                {
                    'organizationId': ObjectId(organisation_id),
                    'isDeleted': False,  # Nur Einträge, bei denen isDeleted auf False ist
                    'licensePlate': {'$exists': True, '$ne': ''}
                },
                {'_id': 1, 'licensePlate': 1,"class":1,"model":1,"brand":1,"type":1,"grossVehicleWeightRating":1}
            )
        )
        plate_dict = {}
        for entry in list_plates:
            plate_dict[entry['licensePlate']] = {
                'id': str(entry['_id']),
                'model': entry.get('model', ''),
                'brand': entry.get('brand', ''),
                'type': entry.get('type', ''),
                'class': entry.get('class', ''),
                'grossVehicleWeightRating': round(entry.get('grossVehicleWeightRating', 0) / 1000, 1) if entry.get(
                    'grossVehicleWeightRating', 0) > 100 else round(entry.get('grossVehicleWeightRating', 0), 1)

            }

        return plate_dict

    def get_vehicle_By_Id(self, id):
        vehicle_doc = self.collection.find_one({'_id': ObjectId(id)})

        if vehicle_doc:
            vehicle_object = Vehicle(
                _id=vehicle_doc['_id'],
                type=vehicle_doc.get('type', ''),
                model=vehicle_doc.get('model', ''),
                brand=vehicle_doc.get('brand', ''),
                trackedDistance=vehicle_doc.get("statistics.trackedDistance",''),
                urbanPercentage = vehicle_doc.get("statistics.urbanPercentage", ''),
                highwayPercentage = vehicle_doc.get("statistics.highwayPercentage", '')

            )

            result_vehicle = [{
                "vehicle_data_in_fms": {
                    'id': str(vehicle_object._id),
                    'type': str(vehicle_object.type),
                    'model': str(vehicle_object.model),
                    'make': str(vehicle_object.brand),
                    'trackedDistance':str(vehicle_object.trackedDistance),
                    'urbanPercentage':str(vehicle_object.urbanPercentage),
                    'highwayPercentage': str(vehicle_object.highwayPercentage)
                }
            }]

            return result_vehicle
