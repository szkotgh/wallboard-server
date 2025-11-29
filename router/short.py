from flask import Blueprint, redirect, url_for
import db.domain.wall as db_wall

short_bp = Blueprint('short', __name__, url_prefix='/s')

@short_bp.route('/<code>', methods=['GET'])
def resolve_short(code):
    info = db_wall.get_info_by_short_code(code)
    if not info.result:
        return info.to_response()
    wall_id = info.data.get('id')
    return redirect(url_for('wall.get_wall_info', wall_id=wall_id))



