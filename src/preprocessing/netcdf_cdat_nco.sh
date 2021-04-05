ncks --mk_rec_dmn time in.nc out.nc
set str1 = 'time = 1 ;'
set str2 = 'time = UNLIMITED ; // (1 currently)'
ncdump in.nc  | sed -e "s#^.$str1# $str2#" | ncgen -o out.nc
ncecat -O -u time in.nc out.nc
