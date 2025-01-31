import tkinter as tk
from queue import Queue
import threading


root= tk.Tk()
queue1 = Queue()
def websocket_worker(queue):
    while True:
        if not queue.empty():
            event = queue.get()
            print("hallo")

def other_worker(queue):
    while True:
        queue.put(0)
        print("put")


if __name__ == "__main__":
    button_thread = threading.Thread(target=other_worker,args=(queue1,))
    websocket_thread = threading.Thread(target=websocket_worker, args=(queue1,))
    button_thread.start()
    websocket_thread.start()
    root.mainloop()


