from flask import Flask, jsonify
import os
import json
from flask import Flask,request
import whisper
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = whisper.load_model("small")

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route("/download", methods=['POST'])
def download():
  file = request.files['file']
  filterId = request.form.get('filterId')
  userId = request.form.get('userId')

  print('file', file)
  print('filterId', filterId)
  print('userId', userId)

  if file.filename != None:
    print(file.filename)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    result = model.transcribe('./' + filename, verbose=True, language='en')
    os.remove('./' + filename)
    # model.cpu()
    # del model

    requests.post("https://audioscript.vercel.app/api/save-document", data={
        "filterId": filterId,
        "userId": userId,
        "transcriptions": json.dumps(result),
        "fileName": file.filename
    })

    return 'done'

  return 'hello'

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
