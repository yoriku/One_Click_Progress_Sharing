from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import pandas as pd
from connect_db import regi_kintone, get_all_kintone
from Line import send_line

app = Flask(__name__, template_folder='static')
app.secret_key = 'gfshvghenytrhbertb'
socketio = SocketIO(app, async_mode="gevent")

# These codes are redundant or unnecessary and we would like to organize them.
connected_users = set()
master_url = 'your site url'
notification_data = {'name': None, 'job': None, 'uid': None}

api_token = "your kintone api token"

@app.route('/')
def index():
    return render_template('index.html')

# Your task page. This page func is notification and display status.
@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        name = request.form.get('name')
        job = request.form.get('job')
        if(name is not None and job is not None):
            session['name'] = name
            session['job'] = job
            notification_data['name'] = name
            notification_data['job'] = job

            return render_template('task.html', name=name, job=job)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# This page func is diasplay form and notification is sent out depending on the input.
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    print(request.method)
    if request.method == 'POST':
        name = request.form.get('name')
        job = request.form.get('job')

        project = request.form.get('shintyoku')
        question = request.form.get('shitsumon')
        detail = request.form.get('message')
        if name is not None and job is not None:
            project, progress = "ダミー", project
            regi_kintone(api_token, name, job, project, progress, question, detail)

            if (progress == "要対応" or progress == "順調じゃない") and job == "member":
                data = [f'{name}さんを助けましょう！！', '']
                send_line(f'{name}さんを助けましょう！！')
                socketio.emit('notification', {'data': data}, room="manager")

            if (question == "可能" or question == "まあまあ可能") and job == "manager":
                data = [f'{name}さんに質問しましょう！！', '']
                socketio.emit('notification', {'data': data}, room="member")
            # renew_list(name, job, progress, question, detail)
            names, jobs, _, progress, questions, details = get_db_data()
            data = [names, jobs, progress, questions, details]
            socketio.emit('renew_list', {'data': data}, room=notification_data['uid'])

            close_window_script = '''
                <script type="text/javascript">
                    window.close();
                </script>
                '''
            return close_window_script
        else:
            return redirect(url_for('index'))
    else:
        return render_template('form.html')

# get data from kintone
def get_db_data():
    output = get_all_kintone(api_token, norm=True)

    names = []
    jobs = []
    projects = []
    progress = []
    questions = []
    details = [] 
    dateTime = []

    for row in output:
        names.append(row[0])
        jobs.append(row[1])
        projects.append(row[2])
        progress.append(row[3])
        questions.append(row[4])
        details.append(row[5])
        dateTime.append(row[6])
    return names, jobs, projects, progress, questions, details


@socketio.on('connect')
def handle_connect():
    if session.get('name') and session.get('job'):
        join_room(session.get('job'))
        join_room(request.sid)
        notification_data['uid'] = request.sid
        connected_users.add(request.sid)

        start_time = 10
        end_time = 23
        interval = 5
        name = notification_data['name']
        job = notification_data['job']
        if name is not None and job is not None:
            url = f'{master_url}/submit?name={name}&job={job}'
        else:
            url=f'{master_url}/'
        body = f'{name}さん'
        data = [start_time, end_time, interval, '通知', url]

        socketio.emit('schedulednotification', {'data': data}, room=notification_data['uid'])

        # create_list(name, job, progress, question, detail)
        names, jobs, _, progress, questions, details = get_db_data()
        data = [names, jobs, progress, questions, details]
        socketio.emit('create_list', {'data': data}, room=notification_data['uid'])


@socketio.on('disconnect')
def handle_disconnect():
    leave_room(session.get('job'))
    leave_room(request.sid)
    connected_users.remove(request.sid)



def get_data(csv_path= "data/data.csv"):
    data = pd.read_csv(csv_path).values.tolist()
    header = pd.read_csv(csv_path).columns.tolist()
    return header, data


if __name__ == '__main__':
    # socketio.run(app, debug=True, port=1234)
    socketio.run(app, host="0.0.0.0")
