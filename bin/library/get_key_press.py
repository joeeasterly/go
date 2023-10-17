import sys

def get_key_press():
    if sys.platform == 'win32':
        import msvcrt
        return msvcrt.getch().decode('utf-8').lower()
    else:
        import termios, tty, sys
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)