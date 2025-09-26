Real-Time QR Code Attendance System
A smart, automated attendance system built with Python and OpenCV. This project leverages computer vision to scan QR codes from a live webcam feed and logs attendance in real-time. The system is designed around a dynamic, day-specific academic timetable, making it a practical solution for educational institutions to replace manual attendance tracking and generate clean, structured data.

Features
Real-Time QR Code Scanning: Utilizes OpenCV's built-in QR code detector for fast and reliable scanning from a live video feed.
Dynamic Timetable Engine: Operates on a full weekly schedule, automatically identifying the current academic period and subject based on the system's time and date.
Period-Based Attendance: Allows students to mark their attendance once for each specific academic period.
Duplicate Entry Prevention: Prevents a student from marking their attendance more than once during the same period, with feedback provided both on-screen and in the terminal.
Automated CSV Logging: Creates a new, date-stamped CSV file (e.g., attendance_2025-09-26.csv) every day to maintain organized, analysis-ready records.
Live On-Screen Feedback: Provides instant visual feedback on the camera feed, displaying the current period, status messages ("Marked," "You have already marked your attendance."), and break times.
Fully Customizable: The student data, QR code details, and weekly timetable can be easily configured by modifying the Python scripts.

How It Works
generate_qrs.py: A utility script to generate unique QR codes for each student. It embeds their details (Name, Roll No, Department, etc.) into a PNG image file.
attendance_system.py: This is the main application that captures the webcam feed.
It continuously checks the current time against the predefined TIMETABLE.
When a QR code is detected during an active period, the system cross-references it with the attendance_log for that period.
If the student has not yet been marked, their details and a timestamp are appended to the day's CSV file.
Appropriate visual feedback is provided on the screen to confirm the action.

Setup and Usage
Follow these steps to get the project up and running on your local machine.

Prerequisites
Python 3.7+

A webcam connected to your computer.
Installation & Configuration

Clone the repository:
git clone [https://github.com/your-username/qr-attendance-system.git](https://github.com/your-username/qr-attendance-system.git)
Navigate to the project directory:cd qr-attendance-system
Install the required dependencies:
pip install -r requirements.txt

Customize Student Data:
Open the generate_qrs.py file.
Modify the students list to include the details of your students.

Generate QR Codes:
Run the script from your terminal:
python generate_qrs.py

This will create a QRCodeImages folder containing the unique QR code for each student.

Customize the Timetable:
Open the attendance_system.py file.
Modify the TIMETABLE dictionary to match your academic schedule.

Running the Application
Execute the main script from your terminal:
python attendance_system.py

The webcam window will open. Show the generated QR codes to the camera to mark attendance.
Press the 'q' key to close the application.

Sample Output
The system will generate a CSV file named attendance_YYYY-MM-DD.csv with the following structure:

Date,Day,Time,Period,Subject,Details
2025-09-26,Friday,09:05:12 AM,1,GEN AI,"Santhosh, 143, AIML, B"
2025-09-26,Friday,09:05:18 AM,1,GEN AI,"Shiv Shankar, 148, AIML, B"
2025-09-26,Friday,10:01:30 AM,2,I&T AI,"Santhosh, 143, AIML, B"
...

