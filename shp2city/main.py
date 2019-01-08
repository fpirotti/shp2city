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


from argparse import ArgumentParser
from multiple_selection import multiple_selection
from spatial_join_shps import spatial_join


import geopandas as gpd
import pickle
import gml


def main():

    args = parse_args()
    if len(args.shapefiles) ==1:
        joined = gpd.read_file(args.shapefiles[0])
        
    else:
        target = gpd.read_file(args.shapefiles[0])
        join = gpd.read_file(args.shapefiles[1])
        print target.shape
        print join.shape
        print target.iloc()[0]
        print join.iloc()[0]

        op = args.join_operation
        joined = spatial_join(target, join, op)

        #joined = pickle.load(open(file_name, "rb"))
        

    list_attributes = ["Global_ID", "Element_ID", "Building_height_from_terrain", "Temporal_validity", "Scale",\
            "Building_category", "Building_status"]
    title = 'Please choose the column name of your shapefile that represent the following feature: %s'
    # To move from one choice to the next hiting SPACE.\n\
    # Please respect the order of choice of the proposed features list'
    options = list(joined)
    options.append('NA')
    print options

    list_fields, index = multiple_selection(title, options, list_attributes)

    # while index == 1:
    #     options = list(joined)
    #     options.append('NA')
    #     print options
    #     list_fields, index = multiple_selection(title, options, list_attributes)


    # return
    #list_fields = ['CR_EDF_UUI_i', 'UUID', 'UN_VOL_AV', 'MD_UPD_DT_i', 'MD_POSACC_i', 'CR_EDF_CT', 'CR_EDF_ST']
    
    #list_fields = ['OBJECTID', 'NA', 'UN_VOL_AV', 'NA', 'NA', 'NA', 'NA']
    #print dict(zip(list_attributes, list_fields))
    # attr_vs_field = dict(zip(list_attributes, list_fields))

    #gml.build(joined, dict(zip(list_attributes, list_fields)), args.output)
    
    gml.write(joined, dict(zip(list_attributes, list_fields)), args.output)


def parse_args():
    parser = ArgumentParser(description='Convert shapefile into cityGML.')
    parser.add_argument('output', help='path of the output citygml')
    parser.add_argument('join_operation', help='type of join operation to apply between intersects, within or contains')
    parser.add_argument('shapefiles', nargs='+', help='shapefiles to be converted')
    return parser.parse_args()


if __name__ == '__main__':
    main()
