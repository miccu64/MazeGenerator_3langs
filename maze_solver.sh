#!/bin/bash
# Autor: Konrad Micek, informatyka stosowana 1 rok II st.

findMinValue() {
    local -n visitedCellsLocal lengthsLocal
    local min
    visitedCellsLocal=$1
    lengthsLocal=$2

    min=999999
    lengthsLocalLength=${#lengthsLocal[@]}
    for cellIndex in $(seq 1 $lengthsLocalLength); do
        # check if that key exists
        if ! [ "${visitedCellsLocal[${i}]+abc}" ]; then
        currentCell=${lengthsLocal[$cellIndex]}

        if [ [ "$cell" -gt "-1" ] && [ "$cell" -lt "$min" ] ]
    done

}

argvLength=$#
arr=("$@")
if [ "$argvLength" -lt "2" ]; then
    arr=(4 5 0 0 3 3 6 3 3 5 12 4 6 9 10 13 12 4 6 9 8 12 10 3 3 9)
fi

xSize="${arr[0]}"
ySize="${arr[1]}"
xStart="${arr[2]}"
yStart="${arr[3]}"
xEnd="${arr[4]}"
yEnd="${arr[5]}"
grid=("${arr[@]:6}")

declare -A visitedCells
visitedCells["${xStart}x${yStart}]"=0
visitedCellsSize=${#visitedCells[@]}

maxLength=$((($xSize-1) * ($ySize-1)))
lengths=( $(for i in $(seq 1 $maxLength); do echo -1; done) )
arrIndex=$(($xStart + ($yStart * $xSize)))
# initial value for starting cell
lengths["$arrIndex"]=0

counter=0
while [ "$visitedCellsSize" -lt "$maxLength" ]; do
    # current cell index in arr
    arrIndex=$(($xStart + ($yStart * $xSize)))

done
