import mandrill
import time
from subprocess import call


def read_names():
    with open("/restaurants/todays_names.txt", 'r') as file:
        return set(file.read().splitlines())


def main():
    max_retry = 5
    old_names = read_names()
    for retry in range(1, max_retry + 1):
        print 'Retry attempt: {} of {}'.format(retry, max_retry)
        if call("/source/connect_wifi.sh", shell=True):
            time.sleep(5)
            continue
        print("FETCHING LATEST CODE FROM GITHUB")
        if call("/update_code.sh", shell=True):
            time.sleep(5)
            continue
        print("SCRAPING SEAMLESS")
        call("/source/scrape_seamless.sh", shell=True)
        new_names = read_names()
        if not (new_names and new_names != old_names):
            time.sleep(5)
            continue
        print("SENDING SCRAPE RESULTS")
        if call("/source/send_scrape_results.sh", shell=True):
            time.sleep(5)
            continue
        break
    call("/source/sleep_pi.sh")


if __name__ == '__main__':
    main()








