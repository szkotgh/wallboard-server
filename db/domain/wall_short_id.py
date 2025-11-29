import db
import db.domain.wall as db_wall
import utils

def get_wall(short_id) -> utils.ResultDTO:
    try:
        # short_id로 wall 정보를 직접 조회 (원본 ID 노출 방지)
        return db_wall.get_info_by_short_id(short_id)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Internal server error', data={'error': str(e)}, result=False)

def create_short_id(wall_id) -> utils.ResultDTO:
    short_id = utils.gen_hash(4)
    
    try:
        conn = db.create_connection()
        conn.execute('''
            INSERT INTO short_wall_id (wall_id, short_id) VALUES (?, ?)
        ''', (wall_id, short_id))
        conn.commit()
        db.close_connection(conn)
        return utils.ResultDTO(code=201, message='Short ID created', data={'short_id': short_id}, result=True)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Short ID creation failed', data={'detail': str(e)}, result=False)

def get_wall_id_by_short_id(short_id) -> utils.ResultDTO:
    """내부적으로만 사용하는 함수로, short_id로 wall_id를 조회합니다."""
    try:
        conn = db.create_connection()
        short_wall = conn.execute('''
            SELECT wall_id FROM short_wall_id WHERE short_id = ?
        ''', (short_id,)).fetchone()
        db.close_connection(conn)
        
        if not short_wall:
            return utils.ResultDTO(code=404, message='Invalid short ID', result=False)
        
        return utils.ResultDTO(code=200, message='Wall ID found', data={'wall_id': short_wall['wall_id']}, result=True)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Internal server error', data={'error': str(e)}, result=False)