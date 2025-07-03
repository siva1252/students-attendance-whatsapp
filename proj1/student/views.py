from django.shortcuts import render, redirect
from .models import Student, Attendance
import datetime
import pyautogui
import pyperclip
import pygetwindow as gw
import time
from urllib.parse import quote


def focus_whatsapp_window():
    try:
        window = gw.getWindowsWithTitle('WhatsApp')[0]  
        window.activate()
        print("✅ Focused WhatsApp window")
        time.sleep(1)
    except Exception as e:
        print(f"❌ Couldn't focus WhatsApp window: {e}")



def send_whatsapp_msg(phone_number, message):

    focus_whatsapp_window()

    
    encoded_msg = quote(message)
    link = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_msg}"

    
    pyautogui.hotkey('ctrl', 'l') 
    time.sleep(1)

    pyperclip.copy(link)
    pyautogui.hotkey('ctrl', 'v')  
    pyautogui.press('enter')       
    print(f"🔗 Opening chat with {phone_number}")
    time.sleep(15)  

    pyautogui.press('enter')       
    print(f"✅ Message sent to {phone_number}")
    time.sleep(6)  



def mark_attendance(request):
    if request.method == 'POST':
        if not request.session.get('attendance_submitted'):  
            students = Student.objects.all()
            today = datetime.date.today()

            for student in students:
                status = request.POST.get(f'status_{student.id}')

              
                Attendance.objects.create(
                    student=student,
                    status=status,
                    date=today
                )

                if status == 'Absent':
                    msg = f"Dear Parent,\nYour child {student.name} is marked absent today ({today}). Please ensure they are okay."

                    try:
                        send_whatsapp_msg(student.phone_number, msg)
                    except Exception as e:
                        print(f"❌ Error sending to {student.phone_number}: {e}")

            request.session['attendance_submitted'] = True
            return redirect('attendance')
    else:
        request.session['attendance_submitted'] = False

    students = Student.objects.all()
    return render(request, 'attendance.html', {'students': students})