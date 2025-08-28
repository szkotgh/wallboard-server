import db
import db.domain.wall as db_wall
import utils

def create_wall_item(wall_id, title, message, create_ip):
    if not wall_id or not title or not message or not create_ip:
        return utils.ResultDTO(code=400, message='Require parameters missing', result=False)

    if not db_wall.get_info(wall_id).result:
        return utils.ResultDTO(code=404, message='Invalid wall_id', result=False)

    id = utils.gen_uuid()
    try:
        conn = db.create_connection()
        conn.execute('''
            INSERT INTO wall_item (id, wall_id, title, message, create_ip) VALUES (?, ?, ?, ?, ?)
        ''', (id, wall_id, title, message, create_ip))
        conn.commit()
        db.close_connection(conn)
        return utils.ResultDTO(code=201, message='Wall item created', data={'item_id': id}, result=True)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Wall item creation failed', data={'detail': str(e)}, result=False)
    
def get_info(wall_item_id):
    if not wall_item_id:
        return utils.ResultDTO(code=400, message='Require parameters missing', result=False)

    try:
        conn = db.create_connection()
        cursor = conn.execute('''
            SELECT * FROM wall_item WHERE id = ?
        ''', (wall_item_id,))
        row = cursor.fetchone()
        db.close_connection(conn)

        if not row:
            return utils.ResultDTO(code=404, message='Wall item not found', result=False)

        return utils.ResultDTO(code=200, message='Wall item found', data=dict(row), result=True)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Wall item retrieval failed', data={'detail': str(e)}, result=False)
    
def get_list_info(wall_id):
    if not wall_id:
        return utils.ResultDTO(code=400, message='Require parameters missing', result=False)

    if not db_wall.get_info(wall_id).result:
        return utils.ResultDTO(code=404, message='Invalid wall_id', result=False)

    try:
        conn = db.create_connection()
        cursor = conn.execute('''
            SELECT * FROM wall_item WHERE wall_id = ?
        ''', (wall_id,))
        rows = cursor.fetchall()
        db.close_connection(conn)

        if not rows:
            return utils.ResultDTO(code=404, message='No wall items found', result=False)
        
        # Convert each row to a dictionary for JSON serialization
        items = [dict(row) for row in rows]
        items.reverse()
        
        return utils.ResultDTO(code=200, message='Wall items found', data=items, result=True)
    except Exception as e:
        return utils.ResultDTO(code=500, message='Wall items retrieval failed', data={'detail': str(e)}, result=False)