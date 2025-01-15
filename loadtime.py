import requests
import time
import schedule

WEBSITE_URL = "https://example.com"
LOG_FILE = "loading_times.log"

# Function to record loading time
def record_loading_time():
    try:
        start_time = time.time()
        response = requests.get(WEBSITE_URL, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        load_time = time.time() - start_time
        log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {load_time:.2f} seconds\n"
        print(log_message.strip())
        
        # Append the log message to the log file
        with open(LOG_FILE, "a") as log:
            log.write(log_message)
    except requests.exceptions.RequestException as e:
        error_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Error: {e}\n"
        print(error_message.strip())
        with open(LOG_FILE, "a") as log:
            log.write(error_message)

# Schedule the task 10 times a day
for hour in range(0, 24, 2):  # Adjust as needed for your schedule
    schedule.every().day.at(f"{hour:02d}:00").do(record_loading_time)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
