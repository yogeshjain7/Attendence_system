import qrcode
import os

# --- Create a directory to store QR codes if it doesn't exist ---
output_dir = "QRCodeImages"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory '{output_dir}' created.")

# --- List of students with their details ---
# You can easily add more students to this list.
students = [
    {"roll_no": "143", "name": "santhosh", "dept": "AIML", "section": "B"},
    {"roll_no": "184", "name": "yogesh", "dept": "AIML", "section": "B"},
    {"roll_no": "148", "name": "shiv shankar", "dept": "AIML", "section": "B"},
    {"roll_no": "186", "name": "Fayzan", "dept": "AIML", "section": "B"}
]

# --- Generate and save a QR code for each student ---
print("Generating QR codes...")
for student in students:
    # Combine the student details into a single string for the QR code
    # Format: RollNo-Name-Dept-Section
    data_to_encode = f"{student['roll_no']}-{student['name']}-{student['dept']}-{student['section']}"
    
    # The filename will be based on the roll number and name for uniqueness
    file_name = f"{student['roll_no']}_{student['name'].replace(' ', '_')}.png"

    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add the formatted data to the QR code
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to the output directory
    file_path = os.path.join(output_dir, file_name)
    img.save(file_path)
    print(f"Successfully generated QR code for {student['name']} at {file_path}")

print("\nAll QR codes generated successfully!")

