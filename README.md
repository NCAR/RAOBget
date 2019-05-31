# RAOBget

This repository contains scripts to download RAOBS from the University of
Wyoming Radiosonde Archive by building URLs like:

 * To download TEXT:LIST data:
```
http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2019&MONTH=05&FROM=2812&TO=2812&STNM=72672
```
 * To download GIF:SKEWT images:
```
http://weather.uwyo.edu/upperair/images/2019052812.72672.skewt.parc.gif
```

The code requires a list of stations. station-query.html copied from https://github.com/NCAR/MTP-VB6/tree/master/config_files/RAOB/BIN/station-query.html

To manually run all unittests:
```
> python3 -m unittest -v
```
