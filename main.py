from recorder.index import Recorder
from time import sleep

def main():
    recorder = Recorder()
    try:
        while L := (recorder.driver.current_url): 
            print(L)
            sleep(5)
    except Exception as e:
        print('quit')


if __name__ == "__main__":
    main()
