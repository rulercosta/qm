from pathlib import Path

class PathManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        self.root_path = Path(__file__).parent.parent.parent.resolve()
        self.static_path = self.root_path / 'static'
        self.templates_path = self.root_path / 'templates'
        self.logs_path = self.root_path / 'logs'
        
        # Add admin paths
        self.admin_path = self.root_path / 'admin'
        self.admin_templates_path = self.admin_path / 'templates'
        self.admin_static_path = self.admin_path / 'static'
        
        # Ensure critical directories exist
        self.logs_path.mkdir(exist_ok=True)
        self.static_path.mkdir(exist_ok=True)
        self.templates_path.mkdir(exist_ok=True)
        self.admin_templates_path.mkdir(exist_ok=True)
        self.admin_static_path.mkdir(exist_ok=True)
    
    def get_template_path(self, *parts):
        """Safely resolve template paths"""
        path = self.templates_path.joinpath(*parts)
        if not path.is_file():
            raise FileNotFoundError(f"Template not found: {path}")
        return str(path)
    
    def get_static_path(self, *parts):
        """Safely resolve static file paths"""
        path = self.static_path.joinpath(*parts)
        if not path.is_file():
            raise FileNotFoundError(f"Static file not found: {path}")
        return str(path)

paths = PathManager()
