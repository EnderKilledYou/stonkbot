from sharp import Sharp, naming

sharp_api = Sharp(app, prefix="/api", naming=naming.file_based)