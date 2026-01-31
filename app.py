import smtplib
import ssl
from email.message import EmailMessage
import time
from datetime import datetime

# --- Configuration (replace with your details or environment variables) ---
sender_email = "your_email@gmail.com"
receiver_email = "recipient_email@example.com" # Can be the same as sender
app_password = "your_generated_app_password" # Use the App Password, not your main password

# Email content
subject = "Medicine Reminder"
body = "Hi there,\n\nThis is a reminder to take your medicine now."

def send_reminder_email(to_email_address):
    """Sends a medicine reminder email."""
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email_address

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            print(f"[+] Email sent successfully to {to_email_address} at {datetime.now().strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"[-] Failed to send email. Error: {e}")

# --- Scheduling Logic ---
def schedule_daily_reminder(reminder_time_str):
    """
    Schedules a daily reminder email.
    
    Args:
        reminder_time_str: The time to send the reminder in "HH:MM" format (e.g., "09:00").
    """
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == reminder_time_str:
            print(f"It's {now}, time for your medicine!")
            send_reminder_email(receiver_email)
            # Wait for 60 seconds to avoid sending multiple emails in the same minute
            time.sleep(60) 
        # Check frequently to catch the target minute
        time.sleep(10) 

# Run the reminder script
if __name__ == '__main__':
    # Set the desired time for the reminder, e.g., "09:00" for 9:00 AM
    reminder_time = "09:00" 
    print(f"Medicine Reminder script started. Waiting for {reminder_time} daily.")
    schedule_daily_reminder(reminder_time)




















