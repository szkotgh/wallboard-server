from flask import Blueprint
from router.wall import wall_bp
from router.wall_item import wall_item_bp

router_bp = Blueprint('router', __name__)
router_bp.register_blueprint(wall_bp)
router_bp.register_blueprint(wall_item_bp)