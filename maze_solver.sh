#!/bin/bash
# Autor: Konrad Micek, informatyka stosowana 1 rok II st.
# using Dijkstra's algorithm

findMinValue() {
    local -n visitedCellsArrayLocal lengthsArrayLocal
    local min
    visitedCellsArrayLocal=$1
    lengthsArrayLocal=$2

    local min=9999999
    local indexOfMin=-1
    local lengthsLocalLength=${#lengthsArrayLocal[@]}
    lengthsLocalLength=$((lengthsLocalLength - 1))
    for cellIndex in $(seq 0 $lengthsLocalLength); do
        cell=${lengthsArrayLocal[$cellIndex]}
        # check value and check if key exists
        if [ "$cell" -gt "-1" ] && [ "$cell" -lt "$min" ] && ! [ "${visitedCellsArrayLocal[${cellIndex}]+abc}" ]; then
            min=$cell
            indexOfMin=$cellIndex
        fi
    done

    # results in Bash are returned by echo
    echo "$indexOfMin"
}

checkAdjacency() {
    # return allows to return nums from 0 to 255
    # in my code 2 - true, 3 - false, to not confuse 0/1 as typical bool, bcs status 0 is success there
    local cell1Local=$1
    local cell2Local=$2
    local xSizeLocal=$3
    local ySizeLocal=$3

    local maxIndex=$((xSizeLocal * ySizeLocal - 1))
    if [ "$cell1Local" -gt "$maxIndex" ] || [ "$cell2Local" -gt "$maxIndex" ] || [ "$cell1Local" -lt "0" ] || [ "$cell2Local" -lt "0" ] || [ "$cell1Local" -eq "$cell2Local" ]; then
        return 3
    fi

    # Bash automatically floor numbers
    local cell1Row=$((cell1Local / xSizeLocal))
    local cell2Row=$((cell2Local / xSizeLocal))
    local xDifference=$((cell1Local - cell2Local))

    if { [ "$xDifference" -eq "-1" ] || [ "$xDifference" -eq "1" ]; } && [ "$cell1Row" -eq "$cell2Row" ]; then
        return 2
    fi

    local yDifference1=$((cell1Local - xSizeLocal))
    local yDifference2=$((cell1Local + xSizeLocal))

    if [ "$yDifference1" -eq "$cell2Local" ] || [ "$yDifference2" -eq "$cell2Local" ]; then
        return 2
    fi
    
    return 3
}

argvLength=$#
grid=("$@")
if [ "$argvLength" -lt "2" ]; then
    grid=(4 5 0 0 3 3 6 3 3 5 12 4 6 9 10 13 12 4 6 9 8 12 10 3 3 9)
fi

xSize="${grid[0]}"
ySize="${grid[1]}"
xStart="${grid[2]}"
yStart="${grid[3]}"
xEnd="${grid[4]}"
yEnd="${grid[5]}"
grid=("${grid[@]:6}")

declare -A visitedCellsArray

lengthsArray=($(for i in $(seq 1 $maxLength); do echo -1; done))
currentIndex=$((xStart + (yStart * xSize)))
# initial value for starting cell
lengthsArray["$currentIndex"]=0
destinationIndex=$((xEnd + (yEnd * xSize)))

counter=0
while [ "$currentIndex" -ne "$destinationIndex" ]; do
    currentIndex="$(findMinValue visitedCellsArray lengthsArray)"
    visitedCellsArray[${currentIndex}]=1

    # find adjacent cells and check if they are connected with this cell
    # left cell
    adjacentIndex=$((currentIndex - 1))

done
