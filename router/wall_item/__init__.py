from flask import Blueprint, request
import db.wall_item
import utils

wall_item_bp = Blueprint('wall_item', __name__, url_prefix='/wall_item')

@wall_item_bp.route('', methods=['GET'])
def get_wall_item_info():
    wall_item_id = request.args.get('wall_item_id', type=str)
    wall_item = db.wall_item.get_info(wall_item_id)
    return wall_item.to_response()

@wall_item_bp.route('/list', methods=['GET'])
def get_wall_item_list_info():
    wall_id = request.args.get('wall_id')
    wall_items = db.wall_item.get_list_info(wall_id)
    return wall_items.to_response()

@wall_item_bp.route('', methods=['POST'])
def create_wall_item():
    wall_id = request.form.get('wall_id')
    title = request.form.get('title')
    message = request.form.get('message')
    create_ip = utils.get_request_ip()
    wall_item = db.wall_item.create_wall_item(wall_id, title, message, create_ip)
    return wall_item.to_response()