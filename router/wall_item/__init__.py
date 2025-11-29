from flask import Blueprint, request
import db.domain.wall_item as db_wall_item
import db.domain.wall_short_id as db_wall_short_id
import utils

wall_item_bp = Blueprint('wall_item', __name__, url_prefix='/wall_item')

@wall_item_bp.route('', methods=['GET'])
def get_wall_item_info():
    wall_item_id = request.args.get('wall_item_id', type=str)
    
    if not wall_item_id:
        return utils.ResultDTO(code=400, message='wall_item_id parameter is required', result=False).to_response()
    
    wall_item = db_wall_item.get_info(wall_item_id)
    return wall_item.to_response()

@wall_item_bp.route('/list', methods=['GET'])
def get_wall_item_list_info():
    wall_short_id = request.args.get('wall_short_id')
    
    if not wall_short_id:
        return utils.ResultDTO(code=400, message='wall_short_id parameter is required', result=False).to_response()
    
    wall_short_id_info = db_wall_short_id.get_wall_id_by_short_id(wall_short_id)
    if wall_short_id_info.result is False:
        return wall_short_id_info.to_response()

    wall_items = db_wall_item.get_list_info(wall_short_id_info.data['wall_id'])
    return wall_items.to_response()

@wall_item_bp.route('', methods=['POST'])
def create_wall_item():
    wall_short_id = request.form.get('wall_short_id')
    title = request.form.get('title')
    message = request.form.get('message')
    
    if not wall_short_id or not title or not message:
        return utils.ResultDTO(code=400, message='wall_short_id, title, and message parameters are required', result=False).to_response()
    
    # short_id로 wall_id 조회
    wall_info = db_wall_short_id.get_wall_id_by_short_id(wall_short_id)
    if wall_info.result is False:
        return wall_info.to_response()
    
    wall_id = wall_info.data['wall_id']
    create_ip = utils.get_request_ip()
    wall_item = db_wall_item.create_wall_item(wall_id, title, message, create_ip)
    return wall_item.to_response()