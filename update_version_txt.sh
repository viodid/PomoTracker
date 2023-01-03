#!/bin/bash

# Store the output of the command in a variable
OUTPUT=$(git describe --tags --always)

# Replace the contents of the file with the output of the command
echo $OUTPUT > version.txt

# Print the output
echo $OUTPUT

