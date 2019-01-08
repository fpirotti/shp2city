# shp2city: program to convert shapefile to cityGML
# Copyright (C) 2018-2019 Francesca Fissore <fissorefrancesca@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from buildings_inits import  *

import geopandas as gpd
import numpy as np


def extract_coords(gdf_geometry):
    return list(gdf_geometry.exterior.coords)


def extract_xy_coords(gdf_geometry):
    return list([xyz[:2] for xyz in extract_coords(gdf_geometry)])


def extract_z_coords(gdf_geometry):
    return list([xyz[-1] for xyz in extract_coords(gdf_geometry)])


def find_bounding_box(shp_file, list_attributes, list_fields):
    field_content = shp_file.iloc()
    h_min = []
    h_max = []
    h_average = []
    for i in range(shp_file.shape[0]):
        h_average_build_on_ground = np.mean(extract_z_coords(field_content[i].geometry))
        h_min_build_on_ground = np.min(extract_z_coords(field_content[i].geometry))
        inits = buildings_inits(field_content[i], list_attributes, list_fields)
        max_height_build = float(inits["Building_height_from_terrain"]) + h_min_build_on_ground
        h_min.append(h_min_build_on_ground)
        h_max.append(max_height_build)
        h_average.append(h_average_build_on_ground)
    point_min = np.append(shp_file.total_bounds[:2], min(h_min))
    point_max = np.append(shp_file.total_bounds[2:], max(h_max))
    return point_min, point_max

# def find_bounding_box(shp_file, list_attributes, list_fields):
#     h_min = []
#     h_max = []
#     h_average = []
#     outdf = gpd.GeoDataFrame(columns=shp_file.columns)
   
#     for idx, row in shp_file.iterrows():
#         inits = buildings_inits(row, list_attributes, list_fields)
#         if row.geometry.type == 'Polygon':
#             outdf = outdf.append(row,ignore_index=True)
#             h_average_build_on_ground = np.mean(extract_z_coords(row.geometry))
#             h_min_build_on_ground = np.min(extract_z_coords(row.geometry))
#             max_height_build = float(inits["Building_height_from_terrain"]) + h_min_build_on_ground
#             h_min.append(h_min_build_on_ground)
#             h_max.append(max_height_build)
#             h_average.append(h_average_build_on_ground)
#         if row.geometry.type == 'MultiPolygon':
#             multdf = gpd.GeoDataFrame(columns=shp_file.columns)
#             recs = len(row.geometry)
#             multdf = multdf.append([row]*recs,ignore_index=True)
#             for geom in range(recs):
#                 multdf.loc[geom,'geometry'] = row.geometry[geom]
#                 h_average_build_on_ground = np.mean(extract_z_coords(row.geometry[geom]))
#                 h_min_build_on_ground = np.min(extract_z_coords(row.geometry[geom]))
#                 max_height_build = float(inits["Building_height_from_terrain"]) + h_min_build_on_ground
#                 h_min.append(h_min_build_on_ground)
#                 h_max.append(max_height_build)
#                 h_average.append(h_average_build_on_ground)
#             outdf = outdf.append(multdf,ignore_index=True)
#     point_min = np.append(shp_file.total_bounds[:2], min(h_min))
#     point_max = np.append(shp_file.total_bounds[2:], max(h_max))
   
#     return point_min, point_max, outdf
    #for i in range(shp_file.shape[0]):
        
    
def polygon_caculation(inits, points_3d):
    polygon = []
    max_h_build = float(inits["Building_height_from_terrain"])  # + grundhoehe
    min_h_ground = np.min([point[2] for point in points_3d])
    roof = []
    ground = []
    for point in points_3d:
        ground.append((point[0], point[1], min_h_ground))
    polygon.append(ground)
    for point in points_3d[::-1]:
        roof.append((point[0], point[1], min_h_ground + max_h_build))
    polygon.append(roof)
    for point_A, point_B in zip(points_3d[:-1], points_3d[1:]):
        surface = []
        surface.append((point_A[0], point_A[1], min_h_ground + max_h_build))
        surface.append((point_B[0], point_B[1], min_h_ground + max_h_build))
        surface.append((point_B[0], point_B[1], min_h_ground))
        surface.append((point_A[0], point_A[1], min_h_ground))
        surface.append((point_A[0], point_A[1], min_h_ground + max_h_build))
        polygon.append(surface)
    return polygon


