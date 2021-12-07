from flask import Flask, request, redirect, url_for, jsonify, render_template
from flask_cors import CORS, cross_origin
from video import Video
# from google_drive import Upload
import socket
import time
import uuid

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        if request.form.get('submit_form'):
            your_name = request.form['your_name']
            class_name = request.form['class_name']
            file_name = your_name+'_'+class_name+''+'_{}'.format(uuid.uuid1())

            Video.collect_data(Video, file_name, class_name)
            return render_template('confirm.html', file_name=file_name)

    return render_template('index.html')


@app.route('/save', methods=['GET', 'POST'])
@cross_origin()
def save():
    # if request.method == 'POST':
    #     if request.form.get('save'):
    #         file_name = request.form['filename']
    #         socket.setdefaulttimeout(60*60)
    #         try:
    #             Upload.upload_data(Upload, file_name)
    #             # print(file_name)
    #         except socket.timeout:
    #             print('time out!')
    #         return render_template('index.html')
    return render_template('confirm.html')

if __name__ == '__main__':
    app.run(debug=True)
