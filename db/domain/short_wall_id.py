import db
import db.domain.wall as db_wall
import utils

def get_wall(short_id) -> utils.ResultDTO:
    try:
        conn = db.create_connection()
        wall = conn.execute('''
            SELECT * FROM short_wall_id WHERE short_id = ?
        ''', (short_id,)).fetchone()
        db.close_connection(conn)
        
        if not wall:
            return utils.ResultDTO(code=404, message='Invalid short ID', result=False)

        wall_info = db_wall.get_info(wall['wall_id'])
        return wall_info

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
        return utils.ResultDTO(code=201, message='Wall created', data={'short_id': short_id}, result=True)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Wall creation failed', data={'detail': str(e)}, result=False)