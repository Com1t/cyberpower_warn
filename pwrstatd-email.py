import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, sys, subprocess
from datetime import datetime

def parse_powerpanel():
  output = subprocess.check_output(("/usr/sbin/pwrstat", "-status"), shell=False)
  output = output.split(b'\n')
  data = {}
  raw_data = {}
  for datum in output[10:-2]:
    name = datum[:29].strip(b'.').strip()
    value = datum[31:].strip()
    raw_data[name] = value

  data["inV"] = raw_data[b"Utility Voltage"].split()[0].decode()
  data["outV"] = raw_data[b"Output Voltage"].split()[0].decode()
  data["battery_cap"] = raw_data[b"Battery Capacity"].split()[0].decode()
  data["remain_time"] = raw_data[b"Remaining Runtime"].split()[0].decode()
  data["loadWatts"] = raw_data[b"Load"].split()[0].decode()
  data["loadPct"] = raw_data[b"Load"].split()[1].split(b'(')[1].decode()

  return data

def send_warning(power_event, event_warning):
  dt_string = datetime.now().strftime("%Y/%m/%d %H:%M")

  sender_email = "<sender email>"
  sender_password = "<sender password>"

  message = MIMEMultipart()
  message["To"] = "<recipient email>"
  message["From"] = sender_email
  message["Subject"] = f"PowerPanel Notification - [{power_event}]"

  ups_stat = parse_powerpanel()

  title = f"<b> {message} </b>"
  messageText = MIMEText(f"""
                {event_warning}
                Time: {dt_string}
                Utility Voltage: {ups_stat["inV"]}
                Output Voltage: {ups_stat["outV"]}
                Battery capacity: {ups_stat["battery_cap"]} %
                Ramining time: {ups_stat["remain_time"]} min.
                Load: {ups_stat["loadWatts"]} Watt({ups_stat["loadPct"]} %)
                """)
  message.attach(messageText)

  server = smtplib.SMTP("smtp.gmail.com:587")
  server.ehlo("Gmail")
  server.starttls()
  server.login(sender_email, sender_password)
  fromaddr = message["From"]
  toaddrs  = message["To"]
  server.sendmail(fromaddr, toaddrs, message.as_string())

  server.quit()
  return

if __name__ == "__main__":
  # data = parse_powerpanel()
  # print(data)
  if len(sys.argv) > 1:
    power_event = sys.argv[1]
    event_warning = sys.argv[2]
  else:
    power_event = "TEST"

  send_warning(power_event, event_warning)
