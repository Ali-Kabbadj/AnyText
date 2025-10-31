EXCLUDED_DIRS = {
    # Version Control
    ".git",
    ".svn",
    ".hg",
    # Python specific
    "__pycache__",
    "venv",
    ".venv",
    "build",
    "dist",
    "eggs",
    "*.egg-info",
    # Node.js specific
    "node_modules",
    # IDE / Editor specific
    ".vscode",
    ".idea",
    # web
    "node_modules",
    ".next",
    ".github",
    ".gitmodules",
}

EXCLUDED_EXTENSIONS = {
    # Compiled/Object files
    ".pyc",
    ".pyo",
    ".pyd",
    ".o",
    ".a",
    ".so",
    ".lib",
    ".dll",
    ".exe",
    ".class",
    # Archives
    ".zip",
    ".tar",
    ".gz",
    ".rar",
    ".7z",
    ".bz2",
    # Media files
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".svg",
    ".ico",
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
    # Documents
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    # Database files
    ".db",
    ".sqlite3",
    # OS-specific
    ".DS_Store",
    "Thumbs.db",
    # web
    "package-lock.json",
}

GENERIC_FILENAMES = {
    "__init__.py",
    "README.md",
    "requirements.txt",
    "Dockerfile",
    "LICENSE",
    ".gitignore",
    "pyproject.toml",
}
