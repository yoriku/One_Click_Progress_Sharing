import requests, json


def extract_latest_records(data):
    latest_data = {}
    
    for row in data:
        name = row[0]
        time = row[-1]
        
        if name not in latest_data or time > latest_data[name][-1]:
            latest_data[name] = row

    data = []
    for key in latest_data.keys():
        data.append(latest_data[key])

    return data


def sel_data(response, mask=["name", "job", "project", "progress", "question", "detail", "作成日時"]):
    response = json.loads(response)

    r = []
    tmp = response['records']
    for i in range(len(tmp)):
        rt = []
        for m in mask:
            data = tmp[i][m]['value']
            rt.append(data)
        r.append(rt)
    r = extract_latest_records(r)
    return r

def get_kintone(api_token):
    """kintoneのレコードを1件取得する関数"""
    url = "https://sample.cybozu.com/k/v1/record.json?app=1&id=1"
    headers = {"X-Cybozu-API-Token": api_token}
    resp = requests.get(url, headers=headers)
    return resp

def get_all_kintone(api_token, norm=True):
    """kintoneのレコードを1件取得する関数"""
    url = "https://sample.cybozu.com/k/v1/records.json?app=1"
    headers = {"X-Cybozu-API-Token": api_token}
    resp = requests.get(url, headers=headers).text
    if norm:
        resp = sel_data(resp)  
    return resp

def regi_kintone(api_token, name, job, project, progress, question, detail):
    """kintoneのレコードを1件取得する関数"""
    url = "https://sample.cybozu.com/k/v1/record.json"
    headers = {"X-Cybozu-API-Token": api_token}
    data = {"app": 1,
            "record": {
                "name": {"value": name},
                "job": {"value": job},
                "project": {"value": project},
                "progress": {"value": progress},
                "question": {"value": question},
                "detail": {"value": detail}
                }
            }
    resp = requests.post(url, headers=headers, json=data)
    return resp

if __name__ == "__main__":
    print("you should get kintone api token!!")

    
