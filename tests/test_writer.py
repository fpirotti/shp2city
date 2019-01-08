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

import pytest

from streaming.writer import StreamingGml, InvalidNamespace

prefix = '<?xml version="1.0" encoding="utf-8"?>\n<CityModel xmlns="ns">'
suffix = '</CityModel>'

def test_empty_document():
    out = StringIO()

    with StreamingGml(out, {None: 'ns'}) as w:
        pass

    assert prefix + suffix == out.getvalue().strip()


def test_element():
    out = StringIO()

    with StreamingGml(out, {None: 'ns'}) as w:
        w.start_node('cityObjectMember')
        w.end_node('cityObjectMember')

    assert prefix + '<cityObjectMember></cityObjectMember>' + suffix == out.getvalue().strip()


def test_ns_element():
    out = StringIO()

    with StreamingGml(out, {None: 'ns'}) as w:
        w.start_node('description')
        w.end_node('description')

    assert prefix + '<description></description>' + suffix == out.getvalue().strip()


def test_text():
    out = StringIO()

    with StreamingGml(out, {None: 'ns'}) as w:
        w.start_node('description')
        w.text('DESCRIPTION')
        w.end_node('description')

    assert prefix + '<description>DESCRIPTION</description>' + suffix == out.getvalue().strip()


def test_element_attrs():
    out = StringIO()

    with StreamingGml(out, {None: 'ns'}) as w:
        w.start_node('Envelope', {'srsDimension': '3', 'srsName': 'epsg:32632'})
        w.end_node('Envelope')

    assert prefix + '<Envelope srsName="epsg:32632" srsDimension="3"></Envelope>' + suffix == \
           out.getvalue().strip()


def test_element_nested():
    out = StringIO()

    with StreamingGml(out, {None: 'ns'}) as w:
        w.start_node('cityObjectModel')
        w.start_node('description')
        w.text("HELLO")
        w.end_node('description')
        w.end_node('cityObjectModel')

    assert prefix + '<cityObjectModel><description>HELLO</description></cityObjectModel>' + suffix == \
           out.getvalue().strip()


def test_unknown_namespace():
    out = StringIO()

    with pytest.raises(InvalidNamespace):
        with StreamingGml(out, {'ns': 'aaa'}) as w:
            w.start_node('ns:start')
            w.start_node('b:elt')
            w.end_node('ns:start')
