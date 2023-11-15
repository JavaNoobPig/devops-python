import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADD')
EMAIL_PASSWORD = os.environ.get('EMAIL_PWD')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')


def restart_server_and_container():
    # restart linode server
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance,5199{linode server ID}4677)
    nginx_server.reboot()
    # restart the application
    while True:
        nginx_server = client.load(linode_api4.Instance,5199{linode server ID}4677)
        if nginx_server.status == 'running':
            time.sleep(5)
            restart_container()
            break


def send_notification(email_msg):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('172.233{linode server IP}.92.82', username='root', key_filename='C:/Users/User/.ssh/id_rsa')
    # stdin, stdout, stderr = ssh.exec_command('docker ps')
    stdin, stdout, stderr = ssh.exec_command('docker start c02a4bf9f7d7')
    print(stdout.readline())
    ssh.close()
    print('Application restarted')


def monitor_application():
    try:
        response = requests.get('http://17{linode server hostname}om:8080')
        if response.status_code == 200:
        #if False:
            print('Application is running successfully!')
        else:
            print('Application Down. Fix it!')
            msg = f'Application returned {response.status_code}'
            send_notification(msg)
            restart_container()

    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = 'Application not accessible at all.'
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).seconds.do(monitor_application)

while True:
    schedule.run_pending()
