from common_imports import *

# user you're taking
CURRENT_USER = getpass.getuser()

# number of equal(=) to print
NUM = 85

# directories to search
DIRS = [
    "/etc", "/home", "/var", "/opt", "/backup", "/backups"
]

# extensions to find
EXTS = [
    "bak", "swp", "kdbx", "txt"
]

# keywords to find
KEYWORDS = [
    "password", "passwd", "pass", "pwd",
    "db", "sql", "mysql", "sqlite", "mongo", "mongodb", "mariadb", "redis",
]
