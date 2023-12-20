from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
from pprint import pprint

from daily_from_influx import FuelRepository
from get_tracks import TrackRepository
from get_vehicles import VehicleRepository
from get_emission_data import EmissionRepository
from calculation_co2 import calculate_co2_on_time, calculate_co2_on_timespan, calculate_co2_for_every_day_in_year

app = Flask(__name__)
CORS(app)


@app.route('/data/<vehicle_id>', methods=['GET'])
def get_data(vehicle_id):
    track_repo = TrackRepository()
    track_result = track_repo.get_distance_for_static_frames(vehicle_id)

    vehicle_repo = VehicleRepository()
    vehicle_instance = vehicle_repo.get_vehicle_By_Id(vehicle_id)

    result = vehicle_instance + track_result

    return jsonify(result)


@app.route("/data/<vehicle_id>/<hsn_tsn>", methods=['GET'])
def calculate_emissions_timeframe(vehicle_id, hsn_tsn):
    track_repo = TrackRepository()
    track_result = track_repo.get_distance_for_static_frames()

    vehicle_repo = VehicleRepository()
    vehicle_instance = vehicle_repo.get_vehicle_By_Id(vehicle_id)

    hsn = hsn_tsn[0:4]
    tsn = hsn_tsn[4:7]

    emission = EmissionRepository()
    emission_result = emission.get_emission_data(hsn, tsn)

    daily_co2 = calculate_co2_on_time(track_result, emission_result)

    result = vehicle_instance + emission_result + track_result + daily_co2

    return jsonify(result)


@app.route("/data/<vehicle_id>/<hsn_tsn>/<start_date_str>/<end_date_str>", methods=['GET'])
def calculate_emissions_timespan(vehicle_id, hsn_tsn, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    track_repo = TrackRepository(vehicle_id)

    s = datetime.now()
    track_result_frames = track_repo.get_distance_for_static_frames(vehicle_id)
    print(datetime.now() - s)
    track_result_span = track_repo.get_distance_for_timespan( start_date, end_date)
    print(datetime.now() - s)

    vehicle_repo = VehicleRepository()
    vehicle_instance = vehicle_repo.get_vehicle_By_Id(vehicle_id)
    print(datetime.now() - s)

    hsn = hsn_tsn[0:4]
    tsn = hsn_tsn[4:7]

    emission = EmissionRepository()
    emission_result = emission.get_emission_data(hsn, tsn)
    print(datetime.now() - s)

    frames_co2 = calculate_co2_on_time(track_result_frames, emission_result)
    print(datetime.now() - s)

    timespan_co2 = calculate_co2_on_timespan(track_result_span, emission_result)
    print(datetime.now() - s)

    result = vehicle_instance + emission_result + track_result_frames + frames_co2 + track_result_span + timespan_co2
    print(datetime.now() - s)

    return jsonify(result)


@app.route("/data/orga/<organisation_id>", methods=['GET'])
def show_license_plate_for_organisations(organisation_id):
    orga_repo = VehicleRepository()
    orga_results = orga_repo.list_licenseplate_for_organisation(organisation_id)
    for i in orga_results:
        pprint(orga_results[i])

    return jsonify(orga_results)


@app.route("/data/<vehicle_id>/<hsn_tsn>/year", methods=['GET'])
def predict_emission_for_year(vehicle_id, hsn_tsn):
    fuel_repo = FuelRepository(vehicle_id)
    fuel_repo.query_influxdb_for_year()
    regres_daily = fuel_repo.calculate()

    for key, value in regres_daily.items():
       pprint({key: value})

    if regres_daily is None:
        hsn = hsn_tsn[0:4]
        tsn = hsn_tsn[4:7]
        track_repo = TrackRepository(vehicle_id)
        emission = EmissionRepository()
        emission_result = emission.get_emission_data(hsn, tsn)
        daily_distances = track_repo.get_daily_distances()
        regres_daily= calculate_co2_for_every_day_in_year(daily_distances, emission_result)



    return jsonify(regres_daily)


app.run()
