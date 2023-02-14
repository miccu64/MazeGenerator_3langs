#!/bin/bash
# Author: Konrad Micek, Applied Computer Science, Bachelors degree 1st year
# solving maze by using Dijkstra's algorithm

findMinValue() {
    local -n visitedCellsArrayLocal lengthsArrayLocal
    local min
    visitedCellsArrayLocal="$1"
    lengthsArrayLocal="$2"

    local min=9999999
    local indexOfMin=-1
    local lengthsLocalLength=$(("${#lengthsArrayLocal[@]}" - 1))
    for cellIndex in $(seq 0 $lengthsLocalLength); do
        cell="${lengthsArrayLocal[$cellIndex]}"
        # check value and check if key exists
        if [ "$cell" -gt "-1" ] && [ "$cell" -lt "$min" ] && ! [ "${visitedCellsArrayLocal[${cellIndex}]+abc}" ]; then
            min="$cell"
            indexOfMin="$cellIndex"
        fi
    done

    # results in Bash are returned by echo
    echo "$indexOfMin"
}

checkIndex() {
    local cell1Local="$1"
    local cell2Local="$2"
    local xSizeLocal="$3"
    local ySizeLocal="$4"

    local maxIndex=$((xSizeLocal * ySizeLocal - 1))
    if [ "$cell1Local" -gt "$maxIndex" ] || [ "$cell2Local" -gt "$maxIndex" ] || [ "$cell1Local" -lt "0" ] || [ "$cell2Local" -lt "0" ]; then
        echo "0"
        return
    fi

    echo "1"
}

getBitFromNumber() {
    local number="$1"
    local bit="$2"

    local D2B=({0..1}{0..1}{0..1}{0..1})
    local binary="${D2B[$number]}"
    echo "${binary:${bit}:1}"
}

checkAdjacency() {
    local index="$1"
    local currentValue="$2"
    local adjacentValue="$3"

    if [ "$currentValue" -lt "0" ] || [ "$adjacentValue" -lt "0" ]; then
        echo "0"
    else
        local result1="0"
        local result2="0"

        # numbers and its walls (same pattern as in Python): 1 -> left, 2 -> right, 4 -> down, 8 -> up
        # bits: 0<up> 1<down> 2<right> 3<left>
        if [ "$index" -eq "0" ]; then
            result1=$(getBitFromNumber "$adjacentValue" 2)
            result2=$(getBitFromNumber "$currentValue" 3)
        elif [ "$index" -eq "1" ]; then
            result1=$(getBitFromNumber "$adjacentValue" 3)
            result2=$(getBitFromNumber "$currentValue" 2)
        elif [ "$index" -eq "2" ]; then
            result1=$(getBitFromNumber "$adjacentValue" 0)
            result2=$(getBitFromNumber "$currentValue" 1)
        else
            result1=$(getBitFromNumber "$adjacentValue" 1)
            result2=$(getBitFromNumber "$currentValue" 0)
        fi

        if [ "$result1" -eq "1" ] && [ "$result2" -eq "1" ]; then
            echo "1"
        else
            echo "0"
        fi
    fi
}

grid=("$@")
for i in "${grid[@]}"; do
    if [ "$i" = "-h" ] || [ "$i" = "--help" ]; then
        echo "Application goal is to generate mazes with size specified by user and allow him to resolve it programmatically."
        echo "Different application parts are built in Python (GUI/languages connector), Perl (generator) and Bash (resolver)."
        echo "Bash solving takes some time - it is Bash, so it obviously have right to be slow :-)"
        echo "After generation, picture is saved as file MazeUnresolved.jpeg."
        echo "After resolving, picture is saved as file MazeResolved.jpeg."
        echo "Picture is also shown in GUI."
        echo "Requirements:"
        echo "For proper working, user should have installed packages PIL (Pillow) and Tkinter."
        echo "User should run application on Linux capable of running GUI."
        echo "For guaranted experience use the newest version of Python."
        exit
    fi
done

argvLength="$#"
if [ "$argvLength" -lt "9" ]; then
    echo "That script won't run separately from Python GUI. Starting Python GUI script instead..."
    ./python_gui.py & exit
fi

xSize="${grid[0]}"
ySize="${grid[1]}"
xStart="${grid[2]}"
yStart="${grid[3]}"
xEnd="${grid[4]}"
yEnd="${grid[5]}"
grid=("${grid[@]:6}")

declare -A visitedCellsArray

maxLength=$((xSize * ySize - 1))
lengthsArray=($(for i in $(seq 0 ${maxLength}); do echo -1; done))
currentIndex=$((xStart + (yStart * xSize)))
# initial value for starting cell
lengthsArray["$currentIndex"]=0
destinationIndex=$((xEnd + (yEnd * xSize)))

while [ "$currentIndex" -ne "$destinationIndex" ]; do
    currentValue="${grid[$currentIndex]}"

    # check if adjacent cells are connected with this cell
    adjacentIndexes=($((currentIndex - 1)) $((currentIndex + 1)) $((currentIndex + xSize)) $((currentIndex - xSize)))
    for index in $(seq 0 3); do
        adjacentIndex=${adjacentIndexes[index]}
        result=$(checkIndex "$currentIndex" "$adjacentIndex" "$xSize" "$ySize")
        if [ "$result" -ne "1" ]; then
            continue
        fi

        adjacentValue="${grid[$adjacentIndex]}"
        result=$(checkAdjacency "$index" "$currentValue" "$adjacentValue")

        if [ "$result" -eq "1" ] && [ "${lengthsArray[$adjacentIndex]}" -lt "0" ]; then
            currentLength=$((lengthsArray["$currentIndex"] + 1))
            lengthsArray["$adjacentIndex"]="$currentLength"
        fi
    done

    # mark as visited cell
    visitedCellsArray["${currentIndex}"]=1
    # find next index
    currentIndex=$(findMinValue visitedCellsArray lengthsArray)
done

# take only shortest path and return its indexes
resultArray=("$destinationIndex")
currentIndex="$destinationIndex"
destinationIndex=$((xStart + (yStart * xSize)))
currentValue="${lengthsArray[$currentIndex]}"
while [ "$currentValue" -ne "0" ]; do
    substrCurrentValue=$((currentValue - 1))
    # check if adjacent cells are connected with this cell
    adjacentIndexes=($((currentIndex - 1)) $((currentIndex + 1)) $((currentIndex + xSize)) $((currentIndex - xSize)))
    for index in $(seq 0 3); do
        adjacentIndex=${adjacentIndexes[index]}
        result=$(checkIndex "$currentIndex" "$adjacentIndex" "$xSize" "$ySize")
        if [ "$result" -ne "1" ]; then
            continue
        fi

        result=$(checkAdjacency "$index" "${grid[$currentIndex]}" "${grid[$adjacentIndex]}")

        adjacentValue="${lengthsArray[$adjacentIndex]}"
        if [ "$result" -eq "1" ] && [ "$substrCurrentValue" -eq "$adjacentValue" ]; then
            currentValue="$adjacentValue"
            resultArray+=("$adjacentIndex")
            currentIndex="$adjacentIndex"
            break
        fi
    done
done

# return results starting with special delimiter
printf '%s' "Results:"
for index in "${resultArray[@]}"; do
    printf '%s' "$index "
done
