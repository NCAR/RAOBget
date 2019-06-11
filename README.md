# RAOBget

This repository contains scripts to download RAOBS from the University of
Wyoming Radiosonde Archive by building URLs like:

 * for accessing TEXT:LIST data:
```
http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2019&MONTH=05&FROM=2812&TO=2812&STNM=72672
```
 * for accessing GIF:SKEWT images:
```
http://weather.uwyo.edu/upperair/images/2019052812.72672.skewt.parc.gif
```

To run the code, use the command:

 * python3 RAOBget.py

The -h option gives a list of parameters you can pass to the code, like requested station id and dates.

To manually run all unittests:
```
> python3 -m unittest -v
```
