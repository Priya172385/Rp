import schedule
import time
from twilio.rest import Client

# --- Configuration ---
# Replace these with your actual Twilio credentials
ACCOUNT_SID = 'your_account_sid_here'
AUTH_TOKEN = 'your_auth_token_here'
TWILIO_NUMBER = 'your_twilio_phone_number'
YOUR_PHONE_NUMBER = 'your_verified_phone_number'

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms_reminder(med_name, dosage):
    """Sends the actual SMS via Twilio API"""
    message_body = f"💊 MEDICINE REMINDER: It's time to take {dosage} of {med_name}."
    
    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
        print(f"[{time.strftime('%H:%M:%S')}] Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending message: {e}")

# --- Scheduling ---
def schedule_meds():
    # Format: .at("HH:MM") in 24-hour format
    # Example 1: Vitamin C at 08:00 AM
    schedule.every().day.at("08:00").do(send_sms_reminder, med_name="Vitamin C", dosage="500mg")
    
    # Example 2: Ibuprofen at 2:30 PM
    schedule.every().day.at("14:30").do(send_sms_reminder, med_name="Ibuprofen", dosage="1 Tablet")

    print("Medicine Scheduler is running... (Press Ctrl+C to stop)")

    while True:
        schedule.run_pending()
        time.sleep(60) # Check every minute

if __name__ == "__main__":
    schedule_meds()

















