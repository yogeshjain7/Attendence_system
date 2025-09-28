import cv2
import numpy as np
from datetime import datetime, time
import csv
import os
import time as timer  # Import timer for message display duration

# --- Full Weekly Timetable ---
# Based on the provided image. You can modify this schedule as needed.
TIMETABLE = {
    "Monday": [
        {"period": 1, "start": time(9, 0), "end": time(9, 55), "subject": "IP&CV"},
        {"period": 2, "start": time(9, 55), "end": time(10, 50), "subject": "E AI"},
        {"period": 3, "start": time(10, 50), "end": time(11, 50), "subject": "NNDL/IPCV LAB"},
        {"period": 4, "start": time(11, 50), "end": time(12, 45), "subject": "NNDL/IPCV LAB"},
        {"period": 5, "start": time(13, 45), "end": time(14, 40), "subject": "GEN AI - SL"},
        {"period": 6, "start": time(14, 40), "end": time(15, 35), "subject": "GEN AI - SL/Project"},
        {"period": 7, "start": time(15, 35), "end": time(16, 30), "subject": "I&T AI - SL/Project"}
    ],
    "Tuesday": [
        {"period": 1, "start": time(9, 0), "end": time(9, 55), "subject": "E AI"},
        {"period": 2, "start": time(9, 55), "end": time(10, 50), "subject": "NN&DL"},
        {"period": 3, "start": time(10, 50), "end": time(11, 50), "subject": "NNDL/IPCV LAB"},
        {"period": 4, "start": time(11, 50), "end": time(12, 45), "subject": "NNDL/IPCV LAB"},
        {"period": 5, "start": time(13, 45), "end": time(14, 40), "subject": "IP&CV - T"},
        {"period": 6, "start": time(14, 40), "end": time(15, 35), "subject": "I&T AI - SL/Project"},
        {"period": 7, "start": time(15, 35), "end": time(16, 30), "subject": "I&T AI - SL/Project"}
    ],
    "Wednesday": [
        {"period": 1, "start": time(9, 0), "end": time(9, 55), "subject": "I&T AI"},
        {"period": 2, "start": time(9, 55), "end": time(10, 50), "subject": "GEN AI"},
        {"period": 3, "start": time(10, 50), "end": time(11, 50), "subject": "NNDL/IPCV LAB"},
        {"period": 4, "start": time(11, 50), "end": time(12, 45), "subject": "NNDL/IPCV LAB"},
        {"period": 5, "start": time(13, 45), "end": time(14, 40), "subject": "NN&DL - T"},
        {"period": 6, "start": time(14, 40), "end": time(15, 35), "subject": "E AI - SL/Project"},
        {"period": 7, "start": time(15, 35), "end": time(16, 30), "subject": "E AI - SL/Project"}
    ],
    "Thursday": [
        {"period": 1, "start": time(9, 0), "end": time(9, 55), "subject": "E-AI"},
        {"period": 2, "start": time(9, 55), "end": time(10, 50), "subject": "GEN AI"},
        {"period": 3, "start": time(10, 50), "end": time(11, 50), "subject": "NN&DL"},
        {"period": 4, "start": time(11, 50), "end": time(12, 45), "subject": "IP&CV"},
        {"period": 5, "start": time(13, 45), "end": time(14, 40), "subject": "I&T AI - T"},
        {"period": 6, "start": time(14, 40), "end": time(15, 35), "subject": "IP&CV - SL/Project"},
        {"period": 7, "start": time(15, 35), "end": time(16, 30), "subject": "IP&CV - SL/Project"}
    ],
    "Friday": [
        {"period": 1, "start": time(9, 0), "end": time(9, 55), "subject": "GEN AI"},
        {"period": 2, "start": time(9, 55), "end": time(10, 50), "subject": "I&T AI"},
        {"period": 3, "start": time(10, 50), "end": time(11, 50), "subject": "IP&CV"},
        {"period": 4, "start": time(11, 50), "end": time(12, 45), "subject": "NN&DL"},
        {"period": 5, "start": time(13, 45), "end": time(14, 40), "subject": "E AI - T"},
        {"period": 6, "start": time(14, 40), "end": time(15, 35), "subject": "NN&DL - SL"},
        {"period": 7, "start": time(15, 35), "end": time(16, 30), "subject": "NN&DL - SL"}
    ],
    "Saturday": [
        {"period": 1, "start": time(9, 0), "end": time(9, 55), "subject": "I&T AI"},
        {"period": 2, "start": time(9, 55), "end": time(10, 50), "subject": "IP&CV"},
        {"period": 3, "start": time(10, 50), "end": time(11, 50), "subject": "GEN AI"},
        {"period": 4, "start": time(11, 50), "end": time(12, 45), "subject": "E AI"},
        {"period": 5, "start": time(13, 45), "end": time(16, 30), "subject": "PROJECT PHASE II"} # Combined periods
    ]
}
LUNCH_START = time(12, 45)
LUNCH_END = time(13, 45)

# --- Function to get the current status (period, lunch, or inactive) ---
def get_current_status(now):
    """Checks the current time against the weekly schedule and returns the current status."""
    current_day_name = now.strftime('%A')
    current_time = now.time()

    # 1. Check for lunch break first
    if LUNCH_START <= current_time < LUNCH_END:
        return {"status": "break", "message": "Lunch Break"}

    # 2. Check for an active period on a scheduled day
    if current_day_name in TIMETABLE:
        todays_schedule = TIMETABLE[current_day_name]
        for period_info in todays_schedule:
            if period_info["start"] <= current_time < period_info["end"]:
                return {"status": "period", "info": period_info}

    # 3. If neither, it's outside class hours
    return {"status": "inactive", "message": "No Active Period"}

# --- Function to write attendance to a date-specific CSV file ---
def mark_attendance(student_data, period_info):
    """Appends student data to a CSV file named with the current date."""
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    day_str = now.strftime('%A')
    time_str = now.strftime('%I:%M:%S %p')
    
    file_path = f"attendance_{date_str}.csv"
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a+', newline='') as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize(file_path) == 0:
            writer.writerow(['Date', 'Day', 'Time', 'Period', 'Subject', 'Details'])
        
        writer.writerow([date_str, day_str, time_str, period_info['period'], period_info['subject'], student_data])
        print(f"Attendance marked for Period {period_info['period']} ({period_info['subject']}): {student_data}")

# --- Main application logic ---
print("Starting Period-Based QR Attendance System...")
print("Press 'q' to exit.")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

detector = cv2.QRCodeDetector()

# Dictionary to keep track of attendance for each period for the current day
attendance_log = {p: set() for day in TIMETABLE.values() for p in range(1, 8)} # Assuming max 7 periods

# --- Variables for managing the on-screen message ---
display_message = ""
message_time = 0
MESSAGE_DURATION = 4 # seconds

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture frame.")
        break
    
    now = datetime.now()
    status = get_current_status(now)

    # Only try to mark attendance if there is an active period
    if status["status"] == "period":
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            current_period_info = status["info"]
            student_data = data
            period_num = current_period_info["period"]
            
            # --- FEATURE: Check if attendance is already marked ---
            if student_data not in attendance_log[period_num]:
                mark_attendance(student_data, current_period_info)
                attendance_log[period_num].add(student_data)
                
                # Set message for successful marking
                display_message = f"Marked: {student_data.split(',')[0]}"
                message_time = timer.time()
            else:
                # Set message for duplicate marking attempt and print to terminal
                print(f"Duplicate scan for Period {period_num}: {student_data}. Cannot Be Marked Again.")
                display_message = "You have already marked your attendance."
                message_time = timer.time()

    # --- Displaying Information on Screen ---
    time_str = now.strftime('%I:%M:%S %p')
    cv2.putText(img, time_str, (img.shape[1] - 250, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the current period status
    if status["status"] == "period":
        period_info = status["info"]
        period_text = f"Period {period_info['period']}: {period_info['subject']}"
        cv2.putText(img, period_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif status["status"] == "break":
        cv2.putText(img, status["message"], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2) # Yellow for break
    else: # inactive
        cv2.putText(img, status["message"], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # --- FEATURE: Display the temporary status message ---
    if display_message and (timer.time() - message_time < MESSAGE_DURATION):
        # Create a black rectangle for the background
        cv2.rectangle(img, (50, img.shape[0] - 100), (img.shape[1] - 50, img.shape[0] - 40), (0,0,0), -1)
        # Put the white message text on top
        cv2.putText(img, display_message, (70, img.shape[0] - 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    else:
        display_message = ""


    cv2.imshow('QR Code Attendance Scanner', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Cleanup ---
print("Shutting down...")
cap.release()
cv2.destroyAllWindows()
print("System shut down successfully.")

