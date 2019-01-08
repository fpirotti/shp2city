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

import geopandas as gpd
import pickle


def spatial_join(target, join, op):
    target = target.dropna()
    join = join.dropna()
    joined = gpd.sjoin(target, join, how="inner", op=op, lsuffix='i', rsuffix='j')
    opt_filename = 'joined.p'
    pickle.dump(joined, open(opt_filename, "wb"))
    return opt_filename

