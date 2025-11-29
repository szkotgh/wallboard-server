import db
import db.domain.wall_short_id as db_short_wall_id
import utils

def create_wall(title, create_ip) -> utils.ResultDTO:
    wall_id = utils.gen_uuid()
    
    try:
        conn = db.create_connection()
        conn.execute('''
            INSERT INTO wall (id, title, create_ip) VALUES (?, ?, ?)
        ''', (wall_id, title, create_ip))
        conn.commit()
        db.close_connection(conn)

        short_info = db_short_wall_id.create_short_id(wall_id)

        return utils.ResultDTO(code=201, message='Wall created', data={'wall_id': wall_id, 'short_id': short_info.data['short_id']}, result=True)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Wall creation failed', data={'detail': str(e)}, result=False)

def delete_wall(wall_id) -> utils.ResultDTO:
    try:
        # Check wall exists
        wall_info = get_info(wall_id)
        if wall_info.result is False:
            return wall_info
        
        # Delete Wall with CASCADE enabled
        conn = db.create_connection()
        # Enable foreign key constraints
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('''
            DELETE FROM wall WHERE id = ?
        ''', (wall_id,))
        conn.commit()
        db.close_connection(conn)
        return utils.ResultDTO(code=200, message='Wall deleted', result=True)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Wall deletion failed', data={'detail': str(e)}, result=False)

def get_info(wall_id) -> utils.ResultDTO:
    try:
        conn = db.create_connection()
        wall = conn.execute('''
            SELECT * FROM wall WHERE id = ?
        ''', (wall_id,)).fetchone()
        db.close_connection(conn)
        if wall:
            wall_info = dict(wall)
            # 원본 ID는 외부로 노출하지 않음
            wall_info.pop('id')
            # IP 주소 마스킹 처리
            if 'create_ip' in wall_info:
                wall_info['create_ip'] = utils.mask_ip_address(wall_info['create_ip'])
            return utils.ResultDTO(code=200, message='Wall info query successful', data=wall_info, result=True)
        else:
            return utils.ResultDTO(code=404, message='Wall not found', result=False)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Internal server error', data={'error': str(e)}, result=False)

def get_info_by_short_id(short_id) -> utils.ResultDTO:
    """short_id로 wall 정보를 조회합니다. 원본 ID는 노출하지 않습니다."""
    try:
        conn = db.create_connection()
        # short_id로 wall_id 조회
        short_wall = conn.execute('''
            SELECT wall_id FROM short_wall_id WHERE short_id = ?
        ''', (short_id,)).fetchone()
        db.close_connection(conn)
        
        if not short_wall:
            return utils.ResultDTO(code=404, message='Invalid short ID', result=False)
        
        # wall 정보 조회 (원본 ID는 노출하지 않음)
        return get_info(short_wall['wall_id'])
    except Exception as e:
        return utils.ResultDTO(code=500, message='Internal server error', data={'error': str(e)}, result=False)