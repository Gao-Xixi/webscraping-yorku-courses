from threading import Thread
from time import sleep, perf_counter
import store
def main():
    thread1 = Thread(target=store.store,args=(85, 100))
    thread2 = Thread(target=store.store,args=(100, 150))
    thread3 = Thread(target=store.store,args=(150, 200))
    thread4 = Thread(target=store.store,args=(200,209))

    threads =[thread1, thread2, thread3, thread4]

    for thread in threads:
            thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_time = perf_counter()

    main()

    end_time = perf_counter()
    print(f'It took {end_time- start_time :0.2f} second(s) to complete.')