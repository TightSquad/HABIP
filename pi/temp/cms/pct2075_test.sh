#!/bin/bash

# Sensor address for Temp Unit
sensor_addr=0x48
# Temperature register
temp_reg=0x00
# I2C Bus
i2c_bus=1

# Hash for hex2binary
declare -A binary_conv
binary_conv=(
["0"]="0000"
["1"]="0001"
["2"]="0010"
["3"]="0011"
["4"]="0100"
["5"]="0101"
["6"]="0110"
["7"]="0111"
["8"]="1000"
["9"]="1001"
["a"]="1010"
["b"]="1011"
["c"]="1100"
["d"]="1101"
["e"]="1110"
["f"]="1111")

# main loop
while true; do
        # read from I2c sensor
        current_temp="$(i2cget -y $i2c_bus $sensor_addr $temp_reg w)"
        # Reorder [LSbyteMSbyte]-->[MSbyteLSbyte]
        temp_reorder="${current_temp:4:2}${current_temp:2:2}"
        # Convert to binary
        temp_bin="${binary_conv[${temp_reorder:0:1}]}${binary_conv[${temp_reorder:1:1}]}${binary_conv[${temp_reorder:2:1}]}${binary_conv[${temp_reorder:3:1}]}"
        # Shift right 5 places --> discards 5 least significant bits
        temp_shifted="${temp_bin:0:11}"
        # Converts binary value to decimal
        temp_dec="$((2#$temp_shifted))"
        # Scale by sensor factor (*0.125) and convert celcius to fahrenheit (*1.8 then +32)
        temp_conv="$(dc -e "$temp_dec 0.125 * 1.8 * 32 + p")"
        # Print converted temperature!
        echo "$temp_conv"F""
        sleep 0.5
done
