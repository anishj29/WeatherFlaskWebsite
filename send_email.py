import smtplib
import ssl


def send_mail(receiver, city, message, weather, alerts):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "programexplorers@gmail.com"
    password = "python2coding"
    message = 'Subject: Weather by Program Explorers\n{}\n\nIn {} Today: \nAlerts:  {}\nWeather:  {} F' \
              '\n\nCheck out our website at  https://weatherprogramexplorer.herokuapp.com' \
        .format(message, city, alerts, weather)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        print("Email sending failed")
    finally:
        server.quit()
