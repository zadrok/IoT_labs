from flask import Flask, render_template
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

'''
PLAYER ID CLASS
'''
class player:
    playerID = uuid.uuid4()

    str(playerID)

if __name__ == '__main__':
    app.run(debug=True)
