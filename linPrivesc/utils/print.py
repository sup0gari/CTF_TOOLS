from constants import NUM

def print_line():
    print("=" * NUM)

def print_banner():
    print(r"""
.__  .__      __________        .__                            
|  | |__| ____\______   \_______|__|__  __ ____   ______ ____  
|  | |  |/    \|     ___/\_  __ \  \  \/ // __ \ /  ___// ___\ 
|  |_|  |   |  \    |     |  | \/  |\   /\  ___/ \___ \\  \___ 
|____/__|___|  /____|     |__|  |__| \_/  \___  >____  >\___  >
             \/                               \/     \/     \/ 
    """)

def print_error(function_name, error):
    print(f"[x] Error in {function_name}(): {type(error).__name__}: {error}")

def initial_banner():
    print_line()
    print_banner()
    print_line()