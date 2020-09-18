from smtplib import SMTP
from ssl import create_default_context


def back_end(receiver, city, message, weather, alerts):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "programexplorers@gmail.com"
    password = "python2coding"
    message = 'Subject: Weather in {}\n{}\n\nToday: \n\nWeather:  {} F \nAlerts:  {}' \
              '\n\nCheck out our website at  https://weatherpe.herokuapp.com'.format(city, message, weather, alerts)

    # Create a secure SSL context
    context = create_default_context()

    # Try to log in to server and send email
    server = SMTP(smtp_server, port)
    try:
        server.starttls(context=context)  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        print("Email sending failed")
    finally:
        server.quit()


def send_mail(receiver, city, message, weather, alerts, is_first):
    if is_first:
        back_end(receiver=receiver, city=city, message=message, weather=weather, alerts=alerts)

    else:
        print('sending')
        back_end(receiver=receiver, city=city, message=message, weather=weather, alerts=alerts)
