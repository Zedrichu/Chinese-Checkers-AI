import sys


def play_beep(duration=700):
    # If running on windows
    if sys.platform.startswith('win'):
        import winsound
        freq = 1000
        winsound.Beep(freq, duration)
