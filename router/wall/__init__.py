from flask import Blueprint, request
import db.wall
import utils

wall_bp = Blueprint('wall', __name__, url_prefix='/wall')

@wall_bp.route('', methods=['GET'])
def get_wall_info():
    wall_id = request.args.get('wall_id')
    wall_info = db.wall.get_info(wall_id)
    return wall_info.to_response()

@wall_bp.route('', methods=['POST'])
def create_wall():
    title = request.form.get('title')
    create_ip = utils.get_request_ip()
    wall = db.wall.create_wall(title, create_ip)
    return wall.to_response()