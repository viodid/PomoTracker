# Get the current month and year
current_month=$(date +%m)
current_year=$(date +%Y)

# Get the last time the file was modified
last_executed=$(stat -c %y script_log.txt | cut -d' ' -f1)

echo $last_executed

# Extract the month and year from the last time the script was executed
last_month=$(echo $last_executed | cut -d'-' -f2)
last_year=$(echo $last_executed | cut -d'-' -f1)

# Compare the current month and year to the month and year of the last time the script was executed
if [ "$current_month" -eq "$last_month" ] && [ "$current_year" -eq "$last_year" ]; then
  # The script was executed in the current month
  echo "The script was executed in the current month"
else
  # The script was not executed in the current month
  bash rewards.sh
fi

