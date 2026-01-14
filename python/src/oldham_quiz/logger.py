DEBUG = True


def info(msg): print(info_str(msg))
def debug(msg):
    if DEBUG: print(debug_str(msg))
def warn(msg): print(warn_str(msg))
def error(msg): print(error_str(msg))
def critical(msg): print(critical_str(msg))
def success(msg): print(success_str(msg))
def log_line(msg): print(log_line_str(msg))

def info_str(msg): return f"\033[34m[INFO] {msg}\033[0m"
def debug_str(msg): return f"\033[36m[DEBUG] {msg}\033[0m"
def warn_str(msg): return f"\033[33m[WARN] {msg}\033[0m"
def error_str(msg): return f"\033[31m[ERROR] {msg}\033[0m"
def critical_str(msg): return f"\033[91m[CRITICAL] {msg}\033[0m"
def success_str(msg): return f"\033[32m[SUCCESS] {msg}\033[0m"
def log_line_str(msg): return f"\033[95m[LOG] {msg}\033[0m"