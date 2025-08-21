import db
import utils

def create_wall(title, create_ip) -> utils.ResultDTO:
    id = utils.gen_hash(4)
    
    try:
        conn = db.create_connection()
        conn.execute('''
            INSERT INTO wall (id, title, create_ip) VALUES (?, ?, ?)
        ''', (id, title, create_ip))
        conn.commit()
        db.close_connection(conn)
        return utils.ResultDTO(code=201, message='Wall created', data={'wall_id': id}, result=True)
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