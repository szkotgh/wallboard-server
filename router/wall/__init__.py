from flask import Blueprint, request
import db.domain.wall as db_wall
import db.domain.wall_short_id as db_short_wall_id
import utils

wall_bp = Blueprint('wall', __name__, url_prefix='/wall')

@wall_bp.route('', methods=['GET'])
def get_wall_info():
    wall_short_id = request.args.get('wall_short_id')
    
    if not wall_short_id:
        return utils.ResultDTO(code=400, message='wall_short_id parameter is required', result=False).to_response()
    
    short_wall_info = db_short_wall_id.get_wall(wall_short_id)
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
    
    if not wall_id:
        return utils.ResultDTO(code=400, message='wall_id parameter is required', result=False).to_response()
    
    # wall_id가 UUID 형식인지 확인 (원본 ID만 허용)
    if len(wall_id) != 36 or not wall_id.count('-') == 4:
        return utils.ResultDTO(code=404, message='Invalid wall ID format. Use original UUID.', result=False).to_response()
    
    delete_info = db_wall.delete_wall(wall_id)
    return delete_info.to_response()