from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('site.html')

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    a1,a2,a3,a4,a5 = data["a1"], data["a2"], data["a3"], data["a4"], data["a5"]
    e1,e2,e3,e4,e5 = data["e1"], data["e2"], data["e3"], data["e4"], data["e5"]
    return jsonify({"a1":a1,"a2":a2,"a3":a3,"a4":a4,"a5":a5})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

@app.route("/calculate2", methods=["POST"])
def calculate2():
    data= request.json
