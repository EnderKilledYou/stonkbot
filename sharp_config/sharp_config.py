
from sharp import Sharp, naming

from app import app

sharp_api = Sharp(app, prefix="/api", naming=naming.file_based)
