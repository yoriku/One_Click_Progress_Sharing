# One_Click_Progress_Sharing
Deliverables of the i-group at the BIPROGY hackathon

# About these programs
新入社員とメンターの方に定期的に現在の状況（課題進捗状況や新入社員の質問に対応できるか）を質問する通知を定期的に送り，お互いの状況を共有しあうことができるWEBアプリです．  
この機能により，新入社員は先輩に質問できる状態であるかを把握することが可能であり，メンターは新入社員の進捗を逐次把握することが可能です．

# Getting Started
1. You should get line notify and Kintone API keys
2. You set Line API key in config/line.txt and Kintone API token in app.py var name is api_token
3. If you run this program in your local computer, you have to use this program in \_\_name\_\_

~~~ Python
socketio.run(app, debug=True, port=1234)
~~~
4. You prepare your virtual env
5. Install Python library in virtual env

~~~ Python
pip install -r requirements.txt
~~~
7. Run app.py

~~~ Python
python app.py
~~~
9. Enter Web site
for example 127.0.0.1:1234
