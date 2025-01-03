***Altimeter***
================
-The Package contains the necessary tools to build and run an altimeter.

-The main script file is simulator.py. The script constructs an altimeter 
as an instance of the Altimeter class and filters raw pressure and gps sensor 
data to perform elevation estimation. 

-The script also runs a version altimeter which does not receive any gps data
and compare it with one which receive gps data. The figures and data are store
in figures and data folder

-Altimeter requires sensors, sensor models and filters which can build as object
of their respective class
