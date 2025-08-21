from flask import Flask
from dotenv import load_dotenv
import os
from router import router_bp
import utils

load_dotenv()

app = Flask(__name__)
app.register_blueprint(router_bp)

@app.errorhandler(404)
def not_found(error):
    dto = utils.ResultDTO(404, 'Not found')
    return dto.to_response()

@app.errorhandler(405)
def method_not_allowed(error):
    dto = utils.ResultDTO(405, 'Method not allowed')
    return dto.to_response()

if __name__ == '__main__':
    app.run(host=os.getenv('HOST_IP'), port=os.getenv('HOST_PORT'), debug=True)