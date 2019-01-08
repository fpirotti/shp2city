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

from cStringIO import StringIO
from datetime import date
from lxml import etree
from shp2city.buildings_inits import buildings_inits
from shp2city.gml.format import element, root, identifier_format, root2
from shp2city.working_on_geometry import find_bounding_box, extract_coords, polygon_caculation
from shp2city.streaming.writer import *
from shp2city.explode import *
global str

def shapefile_cleaning(shpfile, heghlt_label):
    #order shapefile by index
    shpfile = shpfile.sort_index(0)
    #remove duplicated
    shpfile = shpfile[~shpfile.index.duplicated(keep='first')]
    #trasform Multipolygon to polygon
    shpfile_multipoligon = gpd.GeoDataFrame(shpfile[shpfile.geometry.type != 'Polygon'])
    #print 'Num Multipoligon: ',len(shpfile_multipoligon)
    shpfile = shpfile.drop(shpfile_multipoligon.index).append(explode(shpfile_multipoligon))
    #solve probelm with height building: remove shape with height less 0.2 m and converte NaN to 15 m
    shpfile = shpfile.drop(shpfile[shpfile[heghlt_label]<0.2].index)
    shpfile[heghlt_label] = shpfile[heghlt_label].fillna(15.0)
    shpfile = shpfile[~shpfile.index.duplicated(keep='first')]
    return shpfile


# def build(shpfile, attributes,filename):
#     #out = StringIO()
#     with open(filename,'wb') as out:
#         with StreamingGml(out) as w:
#             w.start_node('cityObjectModel')
#             w.start_node('gml:description')
#             w.text("Created by Francesca Fissore")
#             w.end_node('gml:description')
#             w.start_node('gml:name')
#             w.text('LoD1')
#             w.end_node('gml:name')
#             w.end_node('cityObjectModel')
#         glob_id = attributes['Global_ID']
#         heghlt_label = attributes["Building_height_from_terrain"]
#         shpfile = shapefile_cleaning(shpfile, heghlt_label)
#
#         for idx , building_id in enumerate(list(set(shpfile[glob_id]))):
#             shp_layer_grouped = shpfile[shpfile[glob_id] == building_id]
#             dict_building_proberties = {'Global_ID': building_id}
#             if attributes['Element_ID'] == 'NA':
#                 element_id = idx
#                 d = {'Element_ID': element_id}
#                 dict_building_proberties.update(d)
#             if attributes['Scale'] != 'NA':
#                 scale = list(set(shp_layer_grouped[attributes['Scale']]))[0]
#                 d = {'Scale': scale}
#                 dict_building_proberties.update(d)
#
#             if attributes['Building_status'] != 'NA':
#                 building_status = list(set(shp_layer_grouped[attributes['Building_status']]))[0]
#                 d = {'Building_status': building_status}
#                 dict_building_proberties.update(d)
#
#             if attributes['Building_category'] != 'NA':
#                 building_category = list(set(shp_layer_grouped[attributes['Building_category']]))[0]
#                 d = {'Building_category': building_category}
#                 dict_building_proberties.update(d)
#
#             if attributes['Temporal_validity'] != 'NA':
#                 temporal_validity = list(set(shp_layer_grouped[attributes['Temporal_validity']]))[0]
#                 d = {'Temporal_validity': temporal_validity}
#                 dict_building_proberties.update(d)
#             if attributes['Element_ID'] != 'NA':
#                 element_id = list(set(shp_layer_grouped[attributes['Element_ID']]))[0]
#                 d = {'Element_ID': element_id}
#                 dict_building_proberties.update(d)
#
#             building_gml_schema_generic_object(shp_layer_grouped, dict_building_proberties, attributes)
#             break
#         w.end_node('cityObjectModel')
#         #     break
#     return
def build(shpfile, attributes,filename):
    #out = StringIO()
    with open(filename,'wb') as out:
        with StreamingGml(out) as w:
            #w.start_node('cityObjectModel')
            w.start_node('gml:description')
            w.text("Created by Francesca Fissore")
            w.end_node('gml:description')
            w.start_node('gml:name')
            w.text('LoD1')
            w.end_node('gml:name')
            #w.end_node('cityObjectModel')

            glob_id = attributes['Global_ID']
            heghlt_label = attributes["Building_height_from_terrain"]
            shpfile = shapefile_cleaning(shpfile, heghlt_label)

            for idx , building_id in enumerate(list(set(shpfile[glob_id]))):
                shp_layer_grouped = shpfile[shpfile[glob_id] == building_id]
                dict_building_proberties = {'Global_ID': building_id}
                if attributes['Element_ID'] == 'NA':
                    element_id = idx
                    d = {'Element_ID': element_id}
                    dict_building_proberties.update(d)
                if attributes['Scale'] != 'NA':
                    scale = list(set(shp_layer_grouped[attributes['Scale']]))[0]
                    d = {'Scale': scale}
                    dict_building_proberties.update(d)

                if attributes['Building_status'] != 'NA':
                    building_status = list(set(shp_layer_grouped[attributes['Building_status']]))[0]
                    d = {'Building_status': building_status}
                    dict_building_proberties.update(d)

                if attributes['Building_category'] != 'NA':
                    building_category = list(set(shp_layer_grouped[attributes['Building_category']]))[0]
                    d = {'Building_category': building_category}
                    dict_building_proberties.update(d)

                if attributes['Temporal_validity'] != 'NA':
                    temporal_validity = list(set(shp_layer_grouped[attributes['Temporal_validity']]))[0]
                    d = {'Temporal_validity': temporal_validity}
                    dict_building_proberties.update(d)
                if attributes['Element_ID'] != 'NA':
                    element_id = list(set(shp_layer_grouped[attributes['Element_ID']]))[0]
                    d = {'Element_ID': element_id}
                    dict_building_proberties.update(d)

                building_gml_schema_generic_object(shp_layer_grouped, dict_building_proberties, attributes,w)
        #return out
def write(model, filename):
    with open(filename, 'wt') as out:
        model.write(out, xml_declaration=True, encoding='utf-8', pretty_print=True, compression=1 )

def building_gml_schema_generic_object(shp_file, dict_building_proberties, attributes, w):

    num_poligon = shp_file.shape[0]

    if 'init' in shp_file.crs.keys():
        crs = shp_file.crs['init']
    else:
        crs = ''
    point_min, point_max = find_bounding_box(shp_file, attributes.keys(), attributes.values())

    field_content = shp_file.iloc()
    w.start_node('cityObjectMember')
    w.start_node('gen:GenericCityObject')
    w.start_node('gml:boundedBy')
    w.start_node('gml:Envelope', {'srsDimension': '3', 'srsName': crs})
    w.start_node('gml:lowerCorner')
    w.text("%s %s %s" % tuple(point_min))
    w.end_node('gml:lowerCorner')
    w.start_node('gml:upperCorner')
    w.text("%s %s %s" % tuple(point_max))
    w.end_node('gml:upperCorner')
    w.end_node('gml:Envelope')
    w.end_node('gml:boundedBy')
    w.start_node('creationDate')
    w.text(str(date.today()))
    w.end_node('creationDate')

    for key in dict_building_proberties.keys():
        if key != 'Global_ID':
            w.start_node('gen:stringAttribute', {'name': '%s' % key})
            w.start_node('gen:value')
            w.text('%s' % dict_building_proberties[key])
            w.end_node('gen:value')
            w.end_node('gen:stringAttribute')
    w.start_node('gen:lod2Geometry')
    w.start_node('gml:MultiSolid', {'gml:id': 'RLB-'+str(dict_building_proberties['Global_ID'])})
    for i in range(num_poligon):
        inits = buildings_inits(field_content[i], attributes.keys(), attributes.values())
        points_3d = extract_coords(field_content[i].geometry.simplify(0.2))
        polygon = polygon_caculation(inits, points_3d)
        w.start_node('gml:solidMember')
        w.start_node('gml:Solid')
        w.start_node('gml:exterior')
        w.start_node('gml:CompositeSurface')
        for idx, poly in enumerate(polygon):
            w.start_node('gml:surfaceMember')
            w.start_node('gml:Polygon')
            w.start_node('gml:exterior')
            w.start_node('gml:LinearRing')
            for point in poly:
                w.start_node('gml:pos', {'srsDimension':'3'})
                w.text(('%s %s %s') % tuple(point))
                w.end_node('gml:pos')
            w.end_node('gml:LinearRing')
            w.end_node('gml:exterior')
            w.end_node('gml:Polygon')
            w.end_node('gml:surfaceMember')
        w.end_node('gml:CompositeSurface')
        w.end_node('gml:exterior')
        w.end_node('gml:Solid')
        w.end_node('gml:solidMember')
    w.end_node('gml:MultiSolid')
    w.end_node('gen:lod2Geometry')
    w.end_node('gen:GenericCityObject')
    w.end_node('cityObjectMember')
#print out.getvalue()
#return out
