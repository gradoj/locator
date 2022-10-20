from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import json
from scipy.optimize import minimize
from numpy.linalg import norm

def gps_solve(distances_to_station, stations_coordinates):
	def error(x, c, r):
		return sum([(norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

	l = len(stations_coordinates)
	S = sum(distances_to_station)
	# compute weight vector for initial guess
	W = [((l - 1) * S) / (S - w) for w in distances_to_station]
	# get initial guess of point location
	x0 = sum([W[i] * stations_coordinates[i] for i in range(l)])
	# optimize distance from signal origin to border of spheres
	return minimize(error, x0, args=(stations_coordinates, distances_to_station), method='Nelder-Mead').x


'''if __name__ == "__main__":
	stations = list(np.array([[1,1], [0,1], [1,0], [0,0]]))
	distances_to_station = [0.1, 0.5, 0.5, 1.3]
	print(gps_solve(distances_to_station, stations))
'''

class handler(BaseHTTPRequestHandler):
    global test
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
        print('get')
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))


        print(self.path)
        query = urlparse(self.path.encode('ASCII')).query
        print('query',query)

        params=query.split('&')
        print(params)
        stations=[]
        distances=[]
        for param in params:
            if param.find('stations=') >= 0:
                stations = param.split('stations=')[1]
            elif param.find('distances=') >= 0:
                distances = float(param.split('distances=')[1])
            else:
                print('unknown parameter', param)


        print('distances', distances)
        print('stations', stations)
        estimate = gps_solve(distances, stations)
        print('estimate', estimate)

        self.wfile.write(estimate)
        return