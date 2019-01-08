shp2city is a software able to convert cartographic data, containing building information, from ESRI shapefile format to 3D CityGML model.
It supports in input one or multiple ESRI shapefile that used to generate a cityGML file.
In order to perform the conversion process, several parameters should be set by user.
Specifically, the following are requested:
(1) the name of output CityGML file
(2) a spatial relationship parameter, chosen between: “intersects”, “within” or “contains”
(3) paths of inputs files.

The first parameter will be used in the final step in order to save the 3d model.
The second parameter is a fundamental request in order to perform spatial join between multiple files. The choice of this parameter is restricted to three possibilities: i) intersects, ii) contains, iii) within
As for the remaining parameter, it can be composed of paths to one or two shapefiles.
In case there is only one input file, the spatial join step is skipped and the CityGML file will be processed from the single input file purge from null geometries.
In presence of two files, the spatial join process can be performed according to the spatial relation specified as input parameter.

##Installation of the command-line tool
For unix os:
 $ pip install shp2city

To see all the options possible:

 $ shp2city --help



