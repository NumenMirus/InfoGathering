from flask import *
from main import main

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    
    if request.method == 'POST':

        text = request.form.get("taname").split()

        main(text)

        return render_template('index.html', download = True)
        
    return render_template('index.html', download = False)


@app.route("/download", methods = ['POST', 'GET'])
def download():

    if request.method == 'POST':
        return send_file('./Funds_analysis.xlsx')



    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run()