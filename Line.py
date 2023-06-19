import requests

def main():
    send_line("Image Send", "test.jpg")

def import_key(path="config/line.txt"):
    f = open(path, 'r', encoding='UTF-8')
    key = f.read()
    f.close()
    return key

def send_line(message, file_path=None):
    line_notify_token = import_key()
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {message}'}

    if(file_path is None):
        requests.post(line_notify_api, headers = headers, data = data)
    else:
        files = {'imageFile': open(file_path, "rb")}
        line_notify = requests.post(line_notify_api, data=data, headers=headers, files=files)


if __name__ == "__main__":
    main()