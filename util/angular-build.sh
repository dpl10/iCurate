#!/bin/bash
if [ -z "$1" ]; then
	ng build --prod --build-optimizer --aot --base-href $1 ### /files/scientists/dlittle/icurate/
else
	ng build --prod --build-optimizer --aot
fi
