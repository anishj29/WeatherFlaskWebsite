import smtplib
import ssl

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "programexplorers@gmail.com"
password = "python2coding"
receiver_email = "varunk3240@gmail.com"  # Should be changed to the user inputed email in the subscribe bar
msg= "Hello whatsup"

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Can be omitted
    server.starttls(context=context)  # Secure the connection
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()