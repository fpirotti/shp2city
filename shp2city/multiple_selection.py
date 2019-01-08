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

from pick import *


def multiple_selection(title, options, requests):
    list_options = []
    for request in requests:
        option, index = pick(options, (title % request))
        list_options.append(option)
        if option != 'NA':
            options.remove(option)
        else:
            pass
    title2 = 'You have selected: %s \n It is true?' % dict(zip(requests, list_options))
    options2 = ['Yes', 'No']
    option, index = pick(options2, title2)
    return list_options, index

