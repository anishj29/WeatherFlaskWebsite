import smtplib
import ssl


def send_mail(receiver, message):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "programexplorers@gmail.com"
    password = "python2coding"
    receiver_email = receiver  # Should be changed to the user inputed email in the subscribe bar
    message = 'Subject: {}\n\n{}'.format("Weather by Program Explorers", message)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email,receiver_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        print("Email sending failed")
    finally:
        server.quit()

