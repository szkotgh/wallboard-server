from flask import Blueprint, redirect, url_for
import db.domain.wall as db_wall

short_bp = Blueprint('short', __name__, url_prefix='/s')

@short_bp.route('/<code>', methods=['GET'])
def resolve_short(code):
    info = db_wall.get_info_by_short_code(code)
    if not info.result:
        # 404 JSON과 일관되게 처리하려면 앱의 에러핸들러에 맡김
        return info.to_response()
    wall_id = info.data.get('id')
    # 내부 API로 리다이렉트하거나, 프론트 경로가 있다면 거기로 보낼 수 있음
    return redirect(url_for('wall.get_wall_info', wall_id=wall_id))



