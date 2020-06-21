#!/bin/bash

SWAP=99
MEM=19

report()
{
echo "Memory Issue Found"
echo "Swap is: ${SWAP}% Free"
echo "Mem is: ${MEM}% Free"
}

if [ $SWAP -lt 80 -o $MEM -lt 20 ] ; then
		report
else
		echo "NO ISSUES FOUND"
fi
