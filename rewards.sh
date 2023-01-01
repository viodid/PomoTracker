cd ~/PomoTracker/

pipenv run python3 manage.py giveRewards

# Get the current date in the format YYYY-MM-DD
current_date=$(date +%F)

# Print the current date
echo "Crontab executed: $current_date" >> script_log.txt

