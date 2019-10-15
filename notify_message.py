# https://medium.com/@prathamanchan22/send-text-message-sms-in-python-using-fast2sms-a1399e863552
import requests
url = "https://www.fast2sms.com/dev/bulk"

# To get FAST2SMS_APIKEY goto https://www.fast2sms.com
FAST2SMS_APIKEY = ''
DEFAULT_SENDER = ['']


def send_msg(message, phone_numbers):
    phone_numbers = [str(no) for no in phone_numbers]
    phone_numbers = ','.join(phone_numbers)
    headers = {
        'authorization': FAST2SMS_APIKEY,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",}
    payload = f"sender_id=FSTSMS&message={message}&language=english&route=p&numbers={phone_numbers}"
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)


if __name__ == '__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description='Notify through SMS',
                                     formatter_class=RawTextHelpFormatter, )
    parser.add_argument('--mode', '-m', help='1: BOTA script failed \n'
                                             '2: Data Scraping failed', default=1)
    args = vars(parser.parse_args())
    val = int(args['mode'])
    if val == 1:
        message = "CRITICAL: BOTA script failed!"
        send_msg(message, DEFAULT_SENDER)
    elif val == 2:
        message = "Data scraping failed!"
        send_msg(message, DEFAULT_SENDER)
