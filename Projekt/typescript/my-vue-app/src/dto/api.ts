interface VehicleDataInFFms {
    "vehicle_data_in_fms": {
        highwayPercentage: string;
        id: string;
        make: string;
        model: string;
        trackedDistance: string;
        type: string;
        urbanPercentage: string;
    }
}


interface DBVin {
    database_vin: {
        "consumption_l/100km": number;
        name: string;
        vehicle_type: string;
        make: string;
        co2_per_km_in_g: number
    };
}

interface Tracks {
    tracks: {
        total_distance_in_365_days_in_km: number;
        total_distance_in_1_days_in_km: number;
        total_distance_in_7_days_in_km: number;
        last_track_in_km: number;
        total_distance_in_30_days_in_km: number
    };
}

interface Co2Data {
    co2_data: {
        co2_per_km_in_kg: number;
        co2_last_track_in_kg: number;
        co2_last_month_in_kg: number;
        co2_last_week_in_kg: number;
        co2_last_year_in_kg: number;
        co2_last_day_in_kg: number
    };
}

interface DistanceForTimespan {
    distance_for_timespan_in_km: number;
}

interface CalculatedEmissions {
    calculated_emission_for_timespan_in_kg: number;
}

type Co2DataResponse = [VehicleDataInFFms, DBVin, Tracks, Co2Data, DistanceForTimespan, CalculatedEmissions];
