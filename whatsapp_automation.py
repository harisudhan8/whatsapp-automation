import pywhatkit as kit

# Phone number format: '+<country_code><phone_number>'
phone_number = '+919600918451'  # Replace with the actual phone number (including the country code)
message = 'Hello, this is an automated message from Python!'  # The message you want to send
time_hour = 15  # Hour in 24-hour format (e.g., 2 PM is 14)
time_minute = 15 # Minute at which the message should be sent (e.g., 30 minutes)

# Send the WhatsApp message
kit.sendwhatmsg(phone_number, message, time_hour, time_minute)
