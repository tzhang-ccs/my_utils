NetCDF operators (NCOs) for file manipulation and simple calculations



A set of command-line utilities called netCDF operators (NCOs) are available on most of the linux machines, and Mac and PC versions can be downloaded. NCOs permit you to perform simple calculations and manipulations of netCDF or HDF4 files with only a minimal knowledge of the netcdf files. NCOs can be an order of magnitude faster than processing data with matlab or other analysis packages. A set of utilities with similar functionality has been developed at the National Center for Atmospheric Research, and it is called NCAR Command Language. I haven't used it, but I see that it will also make plots of your data.
Useful information on each NCO command can be obtained by just typing the name of the command in your linux session, for example, "ncatted" (no quotes), followed by carriage return. The NCO User's Guide is available in several formats: HTML (User's Guide Index in HTML) and PostScript, PDF, and other, and the users guide is very useful. I strongly urge you to check your calculations a little with other software, for example MATLAB, to make sure that NCO is doing what you think that it is doing. This is especially true with observational data where missing data, and the inumerable ways of writing missing data metadata, can cause you to get incorrect results if you are not careful. Also, if something doesn't work as the manual says it should, you should be sure that you have the latest version of the software. There is also a help forum that you can submit questions to.

Examples of commands:
Pick off a vertical level from NCEP / NCAR reanalysis data
Calculate a time mean or sum over a dimension
Calculate a thickness
Calculate a flux quantity
Simple math and how to change the variable type
Add or modify file attributes
Rename a variable, dimension, or attribute
Concatenating files (appending in time)
Fixing the time variable, Part I: Adding a record dimension.
Fixing the time variable, Part II
Subsetting a region or time, and decimating
Rearranging (flipping, reversing) latitudes
Calculating area averages (producing timeseries)
Calculating vertical averages
Calculate the temporal standard deviation
Eliminate a dimension
Extract a variable
Change the value at one gridpoint
Examples of combinations of commands used to perform common calculations:

Calculate a monthly climatology
Calculate the area between pairs of contours
Please contribute to this WWW page. This file is /home/disk/margaret2/jisao/data/nco/index.html, and you should have write permission.

Examples of commands:
1) The usefulness of these routines is best demonstrated with an example. We get NCEP / NCAR reanalysis data from NOAA CDC in files where values of the variable, for example, geopotential height, are given for all 17 of the model levels. For simplicity it would be nice to have a file of just 500 mb geopotential height. Creating such a file can be done with:
ncea -d level,6,6 -F hgt.mon.mean.nc hgt500.mon.mean.nc
where:

"ncea" stands for netcdf ensemble averager
"-d level,6,6 -F" says take the average along the "level" dimension, and average from level 6 to level 6. The vertical levels in the NCEP NCAR reanalysis are:
1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10
and the 500mb level is the 6th level under FORTRAN-indexing (5th level under C-indexing). The "-F" specfication says to use FORTRAN-indexing.
Return

2) "ncra" could be used to calculate the January climatology of monthly mean data:
ncra -F -d time,1,nmonths,12 hgt.mon.mean.nc hgt.mon.mean.clim.nc
where it now takes the average of every twelfth month and "nmonths" is the total number of months in the file. More generally, the maps to average are specified by "-d dimension,minimum,maximum,stride".
"-F" means use FORTRAN indexing (the numbering begins with 1).
ncra -F -d time,1,,1 input_file output_file will calculate the time mean of a file.
To sum over a dimension, for example to sum a file of daily precipitation to obtain an annual total
ncra -h -O -y ttl in.nc out.nc
will sum in time. I am not sure if this is because time is the record dimension in my file.

Return

3) Calculate thickness.
ncea -F -d level,8,8 hgt.mon.mean.nc hgt300.mon.mean.nc
ncea -F -d level,3,3 hgt.mon.mean.nc hgt850.mon.mean.nc
The NCEP / NCAR reanalysis comes with data for 17 vertical levels. Pick off the data for the 300 and 850 mb pressure levels. -F means use FORTRAN-indexing (indexing begins with 1). C-indexing begins with 0.
ncdiff hgt300.mon.mean.nc hgt850.mon.mean.nc thickness300850.mon.mean.nc
hgt300 - hgt850 --> thickness

Return

4) A more complex calcultaion is to compute pentad-mean (5-day averages) horizontal momentum fluxes, the average of u'v', from the reanalysis daily-average files. The time average momentum flux, [u'v'], can be written as:
[u'v'] = [uv] - [u][v]
where [] and ()' denote time averages and deviations from the time average respectively. In this case the time averages are the averages over 5 days.
With the exception of ncrcat, there are always only one input and one output file in a NCO operation. One way to include two or more input variables in a calculation is to append additional variable files to a file. The reanalysis daily-average data is stored as one year per file. Append vwnd to the uwnd file:
ncks -A vwnd.1948.nc uwnd.1948.nc

Calculate the product uv for a year of daily-average data.
ncap2 -s "uv=uwnd*vwnd" uwnd.1948.nc product.nc
where product.nc will contain uv, uwnd, and vwnd.

[ Brian Mapes provided another way to obtain the product in a file.
### rename variable vwnd to uwnd so ncbo will know to multiply them
ncrename -v vwnd,uwnd vwnd.1948.nc v.1948.nc

### now multiply
ncbo --op_typ=multiply uwnd.1948.nc v.1948.nc uvwnd.1948.nc

### rename the product back to uv, and put in file of same name uv
ncrename -v uwnd,uv uvwnd.1948.nc uv.1948.nc

### mop up
rm uvwnd.* v.*
]

Beginning of pentad loop:
Calculate the pentad means of uv.
ncra -O -F -d time,day1,day2 product.nc product.pentad.nc
where day1 and day2 are the first and last Julian days of the pentad, respectively.

Calculate u'v'.
ncap2 -s "upvp=uv-uwnd*vwnd" -v product.pentad.nc upvp.pentad.nc
where -v forces only upvp (and not uv, uwnd, or vwnd) to be output to upvp.pentad.nc
End of pentad loop

Concatenate the pentad files in a single file for the year.
ncrcat -h -O upvp.pentad.nc upvp.1948.nc

Dan Vimont, now at the University of Wisconson, figured out this calculation. His cshell script for calculating pentad means is linked here (Dan's WWW page).

Return

5) Simple math and how to change the variable type:
i) Suppose you want to perform simple math on a pair of variables. Put the two variables into a single file. This may require
ncks -h -A file_a file_b
which is described elsewhere on this page. Both variables, let's call them A and B, have to be in the same file.

ncap2 -s "AplusB=A+B" -v file_b out.nc
The "-v" option forces only AplusB to be output to out.nc, and the variables A and B are not included in out.nc.

ii) The NCEP / NCAR reanalysis comes as short integers, and NCO tends to write outputs as floating point numbers (which take up twice as much disk space). To convert the floating point numbers back to packed integers, first look at the packing in the original files from CDC, and use these as the add_offset and scale_factor for packing.

For air temperature the add_offset and scale_factor are 512.81 and 0.01, respectively:

ncap2 -O -s "air=(air-512.81)/0.01" filename.nc temp.nc
ncap2 -O -s "air=short(air);air@add_offset=512.81;air@scale_factor=0.01" temp.nc filename.nc

Return

6) For files to be intelligently handled by the Live Access Software, a file needs to have the following defined: units, long_name, and title. In addition, I like to put in an extended history variable.
ncatted -O -a units,air,c,c,"units goes here" filename.nc
where "-a" is followed by "attribute name, variable name, mode (append, create, delete, modify, overwrite), attribute variable type (float, character, ...), attribute value"
ncatted -O -a long_name,air,c,c,"long_name goes here" filename.nc
ncatted -O -h -a title,global,o,c,"title goes here" filename.nc
ncatted -O -h -a history,global,o,c,'history goes here' filename.nc
"\n" (no quotes) can be used to put in a carriage return.

Return

7) This is handy when you obtain a file with unfortunate choices of variable, dimension, or attribute names.
ncrename -h -O -v old_variable_name,new_variable_name filename.nc
-h: do not add to the history variable
-O: (upper case) overwrite the file.
-d oldname,newname: to change a dimension name
-a oldname,newname: to change an attribute name

Return

8) NCO differentiates between concatenating and appending.
If you want to put two variables with the same time dimension into the same file, use
ncks -h -A file_a file_b
will put variables a and b into file file_b

If you have yearly files that you want to concatenate, use
ncrcat -h file_1979 file_1980 file_1981 file_197919801981
ncrcat -h file_1979 file_198[01] file_197919801981
should do the same thing.
-h: do not add to the history variable.*

* There is a special problem that can arise with the time dimension in the concatenated files. I write time as "so many units since some reference time" where the reference time is the first time period present in a file. ncrcat, at present, doesn't calculate the time correctly for files written with the above time prescription, and it provides a non-fatal error. I have come up with a matlab5 work-around where I write correct time values into the time variable inside a matlab session. For example,

f = netcdf( filename, 'write' )
f{'time'}(:) = correct_time_values;
f{'time'}(penultimate:last) = (penultimate and last correct_time_values);
% For reasons that make no sense to me I had to do the previous line.
ncclose( filename ) % You have to "ncclose" the file to write the changes.

Return

9) Fixing the time variable, Part I: Adding a record dimension to a file.
The first question you are asking is "what is a record dimension?" It is becoming common that netCDF files are written for individual months as opposed to larger files with data for a span of months or years. In order to concatenate the files into a single, larger file (see above) with the nco utilities, you need to add a "record dimension" to each file. The triplet of nco commands you need to do this are given on the NCO documentation WWW page (here).

The original file, "in.nc", does not have a record dimension.

ncks --mk_rec_dmn time in.nc out.nc
makes the dimension "time" the record dimension.

The old way to do this (pre 4.0.1) was:

ncecat -O -h in.nc out.nc
ncpdq -O -h -a time,record out.nc out.nc
ncwa -O -h -a record out.nc out.nc

Return

9b) Fixing the time variable, Part II.
Sometimes the file has a time variable that has a value that you want to use in the fixed file. Consider the header and time value of the following file. As with Part I, you need to make time a "record dimension" so that NCOs will concatenate files.

netcdf filename {
dimensions:
        time = 1 ;
        lat = 89 ;
        lon = 180 ;
variables:
        float time(time) ;
                time:units = "days since 1854-01-15" ;
        float data(time,lat,lon)
        ...
data:
 time = 15 ;
}
You want to preserve the time value as you convert "time" to being a record dimension.

set str1 = 'time = 1 ;'
set str2 = 'time = UNLIMITED ; // (1 currently)'
ncdump in.nc  | sed -e "s#^.$str1# $str2#" | ncgen -o out.nc

This script dumps the netcdf file, swaps the time dimension of 1 for "unlimited" time currently 1, and generates a new netCDF file. Someone far more clever than me figured this out. Now you can use NCOs to concatenate files.
Return

10) Subsetting a region or time, and decimating.
Subsetting a region of an array is handled differently than subsetting time.

i) Subsetting a region

Say you have a global dataset, and you only want the data for the northeast portion of the Pacific Ocean.

ncea -d lat,minimum_lat,maximum_lat -d lon,minimum_lon,maximum_lon in.nc out.nc

where "lat" is what latitudes are called your file, and minimum_lat and maximum_lat are latitudes. Integer latitudes/longitudes are treated as indices, and floating point latitudes/longitudes are actual latitudes/longitudes. An example is in the NCO documentation.

If you are using a dateset with wrapped coordinates (sometimes called cyclical boundary conditions), for example the longitudes in a global dataset, and you want to subset across the step jump in the coordinate, ncks will perform the subsetting. An example is where the dataset longitudes span 0 to 360 degrees, and you want to subset a region that includes the Greenwich Meridian.

ncks -d lon,minimum_lon,maximum_lon in.nc out.nc
An example of the above would be a subset for the Sahel in a dataset where longitudes span 0 to 360:
ncks -d lon,340.0,10.0 -d lat,10.0,20.0 in.nc out.nc

ii) Subsetting time.

Subsetting in time can be performed by specifying the actual time written as floating point numbers or the time index values written as integers. Type "ncdump -v time filename.nc" (no quotes) to see what the time values are. If specifying time index values, you need to include the "-F" option if you are counting the first time value as "1". See the NCO documentation. [ Andres Roubicek pointed out the first method. ]

ncea -F -d time,first,last in.out out.nc

iii) Decimating in time or space.

One of the definitions of the word "decimate" is to remove every tenth member of a set, and in data processing the term has come to mean retaining only the nth temporal or spatial gridploint of a dataset. An example of this is if the input file has 3-hourly data and you want to pick off the 00Z observations. This is accomplished with:

ncks -F -d time,1,,8 input.nc output.nc

where "-F" specificies that the counting begins with 1 as opposed to 0, and every 8th time record is kept, beginning with the first record.


Return

11) Reversing (flipping, rearranging) the latitudes in a file.
For most applications it doesn't matter if the data is arranged in the file from southernmost to northernmost latitudes or from northernmost to southernmost latitudes, but it does matter if you are calculating spatial derivatives of a field (the curl in particular). The following will rearrange the latitudes of the data in a file. See the examples in the NCO documentation for more information on what can be done.

ncpdq -O -h -a -lat filename.nc filename.nc

where "-a -lat" means arrange the latitudes by reversing them.

Return

12) Calculating area-averages (producing timeseries)
In the following, "ncwa" is employed to take spatial averages of data. NCOs recognize "_FillValue" but not "missing_value" as the attribute name for missing values. You can add a _FillValue attribute with "ncatted -O -h -a _FillValue,variablename,o,attribute_type,value in.nc out.nc" or rename all the missing_value attributes in a file to _FillValue with "ncrename -a .missing_value,_FillValue in.nc out.nc" (relevant NCO documentation). It is crucial that the attribute type be consistent with the attribute value. The NCO documentation recommends that you have define both _FillValue and missing_value, which seems like a smart idea. All in all I think that it is wise to check your calculation with matlab while you are building confidence in what NCOs are doing and how it is interpreting the file metadata.

Calculate your own "nino3.4" SST index!
ncwa -O -a lat,lon -d lat,-5.0,5.0 -d lon,190.0,240.0 in.nc nino34.nc
Do a ncdump of the the longitude variable to see how longitudes are specified: -180 to 180, or 0 to 360, or something else.
You need to specify the latitudes and longitudes with decimal points or else NCO will interpret the inputs as matrix indices.
Global datasets tend to have longitude ranges of 0 to 360 or -180 to 180. In these respective organizations, there is a way to calculate a mean for a region that includes the Greenwich Meridian or the Dateline. For the case of longitudes spaning 0 to 360, a mean which includes the Greenwich Meridian is calculated with the following.

ncks -d lon,lon_minimum,lat_minimum in.nc out.nc
ncwa -O -a lat,lon out.nc out.nc

where lon_minimum>lon_maximum. An example of this calculation would be an average for the Sahel:

ncks -d lon,340.0,10.0 -d lat,10.0,20.0 in.nc out.nc
ncwa -O -a lat,lon out.nc out.nc
I haven't tried the case of longitudes organized from -180 to 180. One should look at the output of the ncks operation to be sure that you are getting the longitudes that you want.

To calculate an area-averaged index, you first need to add the area weights to the file.
ncap2 -h -O -s "weights=cos(lat*3.1415/180)" in.nc in.nc
ncwa -h -O -w weights -a lat,lon in.nc global_mean.nc

You can also mask some of the grid:
ncwa -h -O -B logical_expression -w weights -a lat,lon in.nc out.nc
The "-B" option stands for binary and an example of the logical_expression could be 'lat > 20' (with single quotes and spaces: not 'lat>20') to calculate the mean for 20-90N. There are other possibilities in the ncwa examples part of the users guide.

Another way to do this is in two steps:
ncks -C -v maskvariablename -A mask.nc in.nc % Adds the mask to out.nc
ncwa -O -h -w maskvariablename -a lat,lon in.nc out.nc



Return
13) Calculate a vertical average
For data in pressure coordinates you have to explicitly tell NCO how to use the pressure data to calculate a vertical average:
ncwa -a pressure_variable_name fnin.nc fnout.nc
will just take the arithmetic mean of fnin.nc at the various pressure levels.

In Matlab, you define a variable of weights for the pressure levels, w, and write it to the netCDF file
ncwrite( fnin.nc, 'w', 'Dimensions', { 'vertical_variable_name', number_of_vertical_levels } )
ncwrite( fnin.nc, 'w', w )

and then use NCO to calculate the vertical mean
ncwa -w w -a vertical_variable_name fnin.nc fnout.nc

to do this from within Matlab:
eval( [ '!ncwa -w w -a vertical_variable_name fnin.nc fnout.nc' ] )

Return

14) Calculate the temporal standard deviation
See the NCO manual on this but, in short, the commands are:

Calculate the time mean of variable_name.
ncwa -O -v variable_name -a time in.nc out.nc
Calculate the deviations with respect to the mean.
ncbo -O -v variable_name in.nc out.nc out.nc
Sum the square of the deviations, divide by (N-1), and take the square root
ncra -O -y rmssdn out.nc out.nc


Return
15) Eliminate a dimension
This may seem like an odd thing to need to do until you need to do it. I wrote a landmask file that unfortunately included time as a dimension landmask(time,lat,lon). This caused confusion when I tried to calculate averages of a variable only over land. To eliminate time, I did the following:

ncwa -a variable_to_eliminate in.nc out.nc

Thank you to Henry Butowski!


Return
16) Extract a variable
To extract a variable from a file and save it as a new file:

ncks -v variable_name in.nc out.nc

Return

17) Change a value at a gridpiont
ncap2 -s 'where(lat==123 & lon==456) {var1=0; var2})' in.nc out.nc

Provided by John of the NCO users group.

Return

July 2016
Todd Mitchell ( mitchell@atmos.washington.edu )
JISAO data
