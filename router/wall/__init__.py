from flask import Blueprint, request
import db.domain.wall as db_wall
import db.domain.wall_short_id as db_short_wall_id
import utils

wall_bp = Blueprint('wall', __name__, url_prefix='/wall')

@wall_bp.route('', methods=['GET'])
def get_wall_info():
    wall_id = request.args.get('wall_short_id')
    
    short_wall_info = db_short_wall_id.get_wall(wall_id)
    return short_wall_info.to_response()

@wall_bp.route('', methods=['POST'])
def create_wall():
    title = request.form.get('title')
    create_ip = utils.get_request_ip()
    
    wall = db_wall.create_wall(title, create_ip)
    return wall.to_response()

@wall_bp.route('', methods=['DELETE'])
def delete_wall():
    wall_id = request.form.get('wall_id')
    
    delete_info = db_wall.delete_wall(wall_id)
    return delete_info.to_response()