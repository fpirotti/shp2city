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


from xml.sax.saxutils import XMLGenerator


XMLNS = {
    None: "http://www.opengis.net/citygml/2.0",
    "app": "http://www.opengis.net/citygml/appearance/2.0",
    "bldg": "http://www.opengis.net/citygml/building/2.0",
    "dem": "http://www.opengis.net/citygml/relief/2.0",
    "frn": "http://www.opengis.net/citygml/cityfurniture/2.0",
    "gen": "http://www.opengis.net/citygml/generics/2.0",
    "gml": "http://www.opengis.net/gml",
    "grp": "http://www.opengis.net/citygml/cityobjectgroup/2.0",
    "luse": "http://www.opengis.net/citygml/landuse/2.0",
    "pfx0": "http://www.citygml.org/citygml/profiles/base/2.0",
    "veg": "http://www.opengis.net/citygml/vegetation/2.0",
    "tex": "http://www.opengis.net/citygml/texturedsurface/2.0",
    "tran": "http://www.opengis.net/citygml/transportation/2.0",
    "wtr": "http://www.opengis.net/citygml/waterbody/2.0",
    "xAL": "urn:oasis:names:tc:ciq:xsdschema:xAL:2.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "sch": "http://www.ascc.net/xml/schematron",
    "smil20": "http://www.w3.org/2001/SMIL20/",
    "smil20lang": "http://www.w3.org/2001/SMIL20/Language",
}


class StreamingGml:
    def __init__(self, fd, xmlns=XMLNS):
        self._fd = fd
        self._namespaces = xmlns

    def __enter__(self):
        self._gen = XMLGenerator(self._fd, 'utf-8')
        self._gen.startDocument()
        self._start_city_model()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._end_city_model()
            self._gen.endDocument()

    def _start_city_model(self):
        namespaces = {
            'xmlns'+('' if nick is None else ':'+nick): url
            for nick, url in self._namespaces.items()
        }

        self._gen.startElement('CityModel', namespaces)

    def _end_city_model(self):
        self._gen.endElement('CityModel')

    def start_node(self, name, attrs={}):
        self._check_namespace(name)
        self._gen.startElement(name, attrs)

    def _check_namespace(self, name):
        idx = name.find(':')
        if idx >= 0:
            ns = name[:idx]
            if ns not in self._namespaces:
                raise InvalidNamespace('no such namespace: %r' % ns)

    def end_node(self, name):
        self._gen.endElement(name)

    def text(self, content):
        self._gen.characters(content)


class InvalidNamespace(Exception):
    """
    You tried to use an undeclared namespace.
    """

