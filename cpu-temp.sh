#!/bin/bash
cpu=$(</sys/class/thermal/thermal_zone0/temp)
cputf=$((cpu/1000*9/5+32))
echo "CPU Temp:" $cputf"'F"
