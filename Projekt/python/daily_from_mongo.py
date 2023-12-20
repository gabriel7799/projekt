from datetime import datetime, timedelta
from tqdm import tqdm
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
from pymongo import MongoClient
from config import mongoConfig
from pprint import pprint


class TrackRepository:
    def __init__(self, vehicle_id):
        self.client = MongoClient(mongoConfig['host'],
                                  username=mongoConfig['username'],
                                  password=mongoConfig['password'],
                                  authSource=mongoConfig['authSource'],
                                  authMechanism=mongoConfig['authMechanism'])

        self.db = self.client['fleet']
        self.collection = self.db['track']
        self.vehicle_id = vehicle_id

        self.distances_daily_dict={}




#  def plot(self):
#      # Plotting the data using matplotlib
#      plt.figure(figsize=(20, 5))
#      plt.plot(self.dates, self.distances, 'o-', color="orange")
#      plt.title(f'Fahrstrecken pro Tag für vehicleID:{vehicle_id}', fontsize=20)
#      plt.xlabel('Datum', fontsize=16)
#      plt.ylabel('Strecke pro Tag in km', fontsize=20)
#
#      # Show only every 20th x-label without overlapping
#      every_nth_label = 20
#      for n, label in enumerate(plt.gca().xaxis.get_ticklabels()):
#          if n % every_nth_label != 0:
#              label.set_visible(False)
#          else:
#              label.set_fontsize(10)
#
#      plt.show()


vehicle_id = "60cda6416a68e6e0e43e8129"
repository = TrackRepository(vehicle_id)
repository.get_daily_distances()
#repository.plot()
