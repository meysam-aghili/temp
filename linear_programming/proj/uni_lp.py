from pulp import LpProblem,LpMinimize,LpVariable,lpSum,PULP_CBC_CMD,value as pulp_value
import folium
from time import time
from pandas import DataFrame,read_csv
from bz2 import open as bz2_open
from networkx import shortest_path,shortest_path_length
from numpy import hstack,newaxis,arange
from sklearn.neighbors import DistanceMetric
from geopandas import GeoDataFrame,points_from_xy
from osmnx import distance,plot_route_folium,load_graphml
import warnings
warnings.filterwarnings('ignore')


class routing():

    def __init__(self,data,graph_file_path,output_file_path):
        
        self.data = data
        self.graph_file_path = graph_file_path
        self.output_file_path = output_file_path
        
    def get_data(self):
        
        df = DataFrame(self.data) 
        df = GeoDataFrame(df, geometry=points_from_xy(df['lon'],df['lat']))
        df.crs = "EPSG:4326"

        return df

    def create_distance_matrix(self,lat, lon):

        haversine = DistanceMetric.get_metric('haversine')
        latlon = hstack((lat[:, newaxis], lon[:, newaxis]))
        dists = haversine.pairwise(latlon)

        return (6371 * dists).astype('int')

    def lp_model(self,df):
        
        n_point = df.shape[0]
        
        distances = self.create_distance_matrix(df.geometry.y,df.geometry.x)
        
        problem = LpProblem('CVRP', LpMinimize)
        x = LpVariable.dicts('x', ((i, j) for i in range(n_point) for j in range(n_point)), lowBound=0, upBound=1, cat='Binary') # edge
        u = LpVariable.dicts('u', (i for i in range(n_point)), lowBound=1, upBound=n_point, cat='Integer') # Nodes
        problem += lpSum(distances[i][j] * x[i, j] for i in range(n_point) for j in range(n_point)) # edge Cost
        for i in range(n_point):
            problem += x[i, i] == 0 # there is no ring
        for i in range(n_point):
            problem += lpSum(x[i, j] for j in range(n_point)) == 1 # only one edge comes out from each node
            problem += lpSum(x[j, i] for j in range(n_point)) == 1 # only one edge enters each node
        for i in range(n_point):
            for j in range(n_point):
                if i != j and (i != 0 and j != 0):
                    problem += u[i] - u[j] <= n_point * (1 - x[i, j]) - 1 # hamband graph
        #print(problem)
        status = problem.solve(PULP_CBC_CMD(maxSeconds=60))

        us_routes_df = DataFrame([[i, j] for i in range(n_point) for j in range(n_point) if pulp_value(x[i, j]) == 1])
        routes = [0]
        for i in range(len(us_routes_df)):
            routes.append(int(us_routes_df[us_routes_df[0]==routes[-1]][1]))
        routes_df = DataFrame(routes,columns=['node_index_id'])
        routes_df['priority'] = arange(routes_df.shape[0])+1
        routes_df.set_index('node_index_id', inplace = True)
        routes_df = GeoDataFrame(df.join(routes_df,how='left'))
        routes_df.crs = "EPSG:4326"
        routes_df.sort_values(by='priority', inplace=True)
        routes_df['lat'] = routes_df['geometry'].y
        routes_df['lon'] = routes_df['geometry'].x
        routes_df.reset_index(drop=True, inplace=True)

        return routes_df

    def get_routes_list(self,routes_df):
        
        with bz2_open(self.graph_file_path, "rb") as fin:
            data = fin.read()
        graph = load_graphml(graphml_str=data)

        routes_list = []
        routes_list_time = []
        routes_lenght = []
        routes_duration = []
        for i in range(len(routes_df)):
            if i != len(routes_df)-1:
                orig_node = distance.nearest_nodes(graph,routes_df.iloc[i]['lon'],routes_df.iloc[i]['lat'])
                dest_node = distance.nearest_nodes(graph,routes_df.iloc[i+1]['lon'],routes_df.iloc[i+1]['lat'])
                l = shortest_path(G=graph, source=orig_node, target=dest_node, weight='length')
                l2 = shortest_path(G=graph, source=orig_node, target=dest_node, weight='travel_time')
                routes_lenght.append(int(shortest_path_length(G=graph, source=orig_node, target=dest_node, weight='length')))
                routes_duration.append(int(shortest_path_length(G=graph, source=orig_node, target=dest_node, weight='travel_time')))
                if i != 0:
                    routes_list += l[1:]
                    routes_list_time += l2[1:]
                else:
                    routes_list += l
                    routes_list_time += l2
        
        return graph, routes_list ,routes_list_time, routes_lenght, routes_duration

    def plot_data(self,graph, routes_list, routes_list_time, routes_df):

        this_map = folium.Map(prefer_canvas=True)
        plot_route_folium(graph, routes_list_time, route_map=this_map, popup_attribute='name', color="#009900", weight=5, name='time')
        plot_route_folium(graph, routes_list, route_map=this_map, popup_attribute='name', color="#0080FE", weight=5, name='lenght')
        folium.GeoJson(data=routes_df[:-1],name='node',tooltip=folium.GeoJsonTooltip(fields= ["priority"],aliases=["priority"],labels=True)).add_to(this_map)
        this_map.fit_bounds(this_map.get_bounds())
        this_map.add_child(folium.map.LayerControl())
        this_map.save(self.output_file_path)

    def run(self):

        print('Started')
        df = self.get_data()
        print('Got Data')
        routes_df = self.lp_model(df)
        print('LP Modeled')
        graph, routes_list, routes_list_time, routes_lenght, routes_duration = self.get_routes_list(routes_df)
        print('Routed')
        self.plot_data(graph, routes_list, routes_list_time, routes_df)
        print('Plotted')
        print('Finished')
        print('total lenght : ',sum(routes_lenght),' meter')
        print('total duration : ',sum(routes_duration),' minutes')

if __name__ == "__main__":

    data1 = {
        'node_type':['dc','point','point','point','point'],
        'lat':[34.8591,34.8069205283399,34.7864722047018,34.7819627101561,34.7906644574943], 
        'lon':[48.533,48.4910542253773,48.4866556882875,48.5231491280914,48.5230141442578]
    }
    data2 = {
        'node_type':['dc','point','point','point','point','point','point','point','point','point','point','point','point','point','point','point','point','point','point'],
        'lat':[34.8591			,	34.8316046939023,	34.8228978181196,	34.8080493661635,	34.7994334608297,	34.7828666698494,	34.7906644574943,	34.7819627101561,	34.7675739146376,	34.7671672220595,	34.7742242261959,	34.7829669516897,	34.7853507335572,	34.7953593675638,	34.8069205283399,	34.8196409556211,	34.8071619417396,	34.8173314710403,	34.8367033586498], 
        'lon':[48.533,48.539198448039,48.5512363918378,48.5651911858679,48.5456425703998,48.5414574378181,48.5230141442578,48.5231491280914,48.5269689774552,48.5101138310113,48.4986695275898,48.5098959677305,48.4988854315506,48.4956127251111,48.4910542253773,48.5023152319877,48.5218864337468,48.5162038973198,48.5101496374482]
    }
    data3 = read_csv(r'.\a.csv',delimiter='\t')
    graph_file_path = r'.\graph_31.graphml.bz2'
    output_file_path = r'.\test.html'
    r = routing(data1, graph_file_path,output_file_path)
    r.run()