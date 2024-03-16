from flask import Flask, Response

app = Flask(__name__)

@app.route('/health')
def gethealth():
    print('Health')
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)