#! /bin/bash

cd /home/alumno/P5
python3 fake_sensor.py -p 5 -gip 192.168.49.2 -gp 30353 -j delicias -la 40.39924909051448 -lo -3.691733697064922 -n Paseo_de_las_Delicias_61 &
python3 fake_sensor.py -p 10 -gip 192.168.49.2 -gp 30354 -j ibiza -la 40.41859360926786 -lo -3.6700943206960157 -n Calle_del_Dr_Esquerdo_46 &
