import os
from flask import Flask,redirect

app = Flask(__name__)

def randomLink():
    randomList = ["https://www.youtube.com/watch?v=qi2oaQjSKQk", "https://www.youtube.com/watch?v=bm909OiPjK8", "https://www.youtube.com/watch?v=vyl5Mwr84MA", "https://www.youtube.com/watch?v=1GgONMugB14", "https://www.youtube.com/watch?v=o48KzPa42_o", "https://www.youtube.com/watch?v=LSj37NGafko", ]

@app.route('/')
def hello():
    return redirect("http://www.example.com", code=302)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)