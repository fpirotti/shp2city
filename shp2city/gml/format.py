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

from lxml import etree


namespaces = {
    None: "http://www.opengis.net/citygml/2.0",
    # "app": "http://www.opengis.net/citygml/appearance/2.0",
    # "bldg": "http://www.opengis.net/citygml/building/2.0",
    # "dem": "http://www.opengis.net/citygml/relief/2.0",
    # "frn": "http://www.opengis.net/citygml/cityfurniture/2.0",
    "gen": "http://www.opengis.net/citygml/generics/2.0",
    "gml": "http://www.opengis.net/gml",
    # "grp": "http://www.opengis.net/citygml/cityobjectgroup/2.0",
    # "luse": "http://www.opengis.net/citygml/landuse/2.0",
    # "pfx0": "http://www.citygml.org/citygml/profiles/base/2.0",
    # "veg": "http://www.opengis.net/citygml/vegetation/2.0",
    # "tex": "http://www.opengis.net/citygml/texturedsurface/2.0",
    # "tran": "http://www.opengis.net/citygml/transportation/2.0",
    # "wtr": "http://www.opengis.net/citygml/waterbody/2.0",
    # "xAL": "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0",
    # "xlink": "http://www.w3.org/1999/xlink",
    # "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    # "sch": "http://www.ascc.net/xml/schematron",
    # "smil20": "http://www.w3.org/2001/SMIL20/",
    # "smil20lang": "http://www.w3.org/2001/SMIL20/Language",
}


# def root(parent, no_namespaces=False):
#     nsmap = None if no_namespaces else namespaces
#     return parent.element("CityModel", nsmap=nsmap)

def root(no_namespaces=False):
    nsmap = None if no_namespaces else namespaces
    return etree.Element("CityModel", nsmap=nsmap)

def root2(xf, no_namespaces=False):
    nsmap = None if no_namespaces else namespaces
    return xf.element("CityModel", nsmap=nsmap)

def element(element_name, parent=None, attributes=None, **kwargs):
    if attributes is None:
        attributes = kwargs
    else:
        attributes.update(kwargs)
    attributes = {qualify_name(k): v for k, v in attributes.items()}

    if parent is None:
        return etree.Element(qualify_name(element_name, always=True), **attributes)
    else:
        return etree.SubElement(parent, qualify_name(element_name, always=True), **attributes)

def qualify_name(name, always=False):
    idx = name.find(':')
    if idx < 0:
        ns = None
    else:
        ns = name[:idx]
        name = name[idx+1:]

    if ns is None and always == False:
        return name
    else:
        urn = namespaces[ns]
        return '{%s}%s' % (urn, name)


def identifier_format(identifier):
    if isinstance(identifier,unicode):
        pass
    else:
        pass#identifier = unicode(hex(identifier))
    identifier= str(identifier)
    if identifier.startswith('RLB'):
        pass
    else:
        identifier = unicode('RLB-'+ str(identifier))

    return identifier
