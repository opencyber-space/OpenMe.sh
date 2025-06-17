from core.starter import run_service
import time

def main():
    while True:
        try:
            run_service()
        except Exception as e:
            time.sleep(30)

if __name__ == "__main__":
    main()
