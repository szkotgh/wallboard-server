import db
import db.domain.short_wall_id as db_short_wall_id
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

def get_info(wall_id) -> utils.ResultDTO:
    try:
        conn = db.create_connection()
        wall = conn.execute('''
            SELECT * FROM wall WHERE id = ?
        ''', (wall_id,)).fetchone()
        db.close_connection(conn)
        if wall:
            return utils.ResultDTO(code=200, message='Wall info query successful', data=dict(wall), result=True)
        else:
            return utils.ResultDTO(code=404, message='Wall not found', result=False)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Internal server error', data={'error': str(e)}, result=False)