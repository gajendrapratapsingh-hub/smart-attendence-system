import cv2
import pandas as pd
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def start_camera():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    attendance = []
    marked = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if not marked:
                name = "Person1"
                date = datetime.now().strftime("%Y-%m-%d")
                time = datetime.now().strftime("%H:%M:%S")
                attendance.append([name, date, time])
                marked = True

        cv2.imshow("Attendance System - Press Q to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if not os.path.exists("attendance"):
        os.makedirs("attendance")

    df = pd.DataFrame(attendance, columns=["Name", "Date", "Time"])
    df.to_csv("attendance/attendance.csv", index=False)
    df.to_excel("attendance/attendance.xlsx", index=False)

    generate_pdf(df)

def generate_pdf(df):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    file_path = "reports/attendance.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 10)

    text.textLine("Attendance Report")
    text.textLine("----------------------------")
    text.textLine("")

    for index, row in df.iterrows():
        text.textLine(f"{row['Name']}    {row['Date']}    {row['Time']}")

    c.drawText(text)
    c.save()
