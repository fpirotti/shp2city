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


from setuptools import setup, find_packages

setup(
    name='shp2city',
    version='0.1.0',
    description='Convert shapefile into cityGML',
    #url='https://github.com/pypa/sampleproject',  # Optional
    author='Francesca Fissore',
    author_email='fissore.francesca@unipd.it',
    packages=find_packages(),
    install_requires=[
        'geopandas',
        'lxml',
        'numpy',
        'pick',
        'rtree'
    ],
    tests_require = [
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'shp2city=shp2city.main:main',
        ],
    },
)
