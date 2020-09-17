import smtplib
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
s.starttls()

        # Authentication
s.login("impulseresults@gmail.com", "sshbash1964")

        # message to be sent
message = "Message_you_need_to_send"

        # sending the mail
s.sendmail("impulseresults@gmail.com", "sabeshnavmuthu@gmail.com", message)

        # terminating the session
s.quit()