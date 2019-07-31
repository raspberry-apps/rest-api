from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from influxdb import InfluxDBClient

app = Flask(__name__)
api = Api(app)
CORS(app)

DB_NAME = 'air_quality'
TIME_FORTMAT = "%Y-%m-%dT%H:%M:%SZ"

def get_client():
    client = InfluxDBClient('localhost', 8086)
    client.switch_database(DB_NAME)
    return client

class GetLastDayReadings(Resource):
    def get(self):
        client = get_client()
        result = client.query('select pm_25, pm_10 from air_quality where time >= now() - 24h order by time asc;')
        client.close()
        return list(result)[0]

class GetVariableDayReadings(Resource):
    def get(self, days):
        client = get_client()
        result = client.query('select pm_25, pm_10 from air_quality where time >= now() - %sd order by time asc;' % days)
        client.close()
        return list(result)[0]

api.add_resource(GetLastDayReadings, '/')
api.add_resource(GetVariableDayReadings, '/days/<days>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
