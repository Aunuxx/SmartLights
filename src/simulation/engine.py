from threading import Thread
from collections.abc import Callable
import time


class Engine:
    def __init__(self) -> None:
        self.thread = EngineThread(lambda:print(".", end=""))
    def start(self) -> None:
        self.thread.start()
    def stop(self) -> None:
        self.thread.stop = True
    def pause(self) -> None:
        self.thread.paused = not self.thread.paused
    def add(self, target: Callable[[],None]) -> int:
        return self.thread.appendTarget(target)
    def remove(self, index: int) -> None:
        self.thread.removeTarget(index)
    def queue(self, target: Callable[[],None], delay: int) -> None:
        self.thread.appendQueue(target, delay)



class EngineThread(Thread):
    def __init__(self, target: Callable[[],None]) -> None:
        self.stop: bool = False
        self.paused: bool = False
        self.targets: list[Callable[[], None]] = [target]
        self.queue: list[tuple[Callable[[], None], int]] = []
        super().__init__(target=lambda:self._call(target))
    
    def _call(self, target: Callable[[],None]) -> None:
        while self.stop == False:
            if self.paused:
                continue
            for t in self.targets:
                t()
            for q in range(len(self.queue)-1,-1,-1):
                tmp = EngineQueue(self.queue[q][0], self.queue[q][1])
                tmp.start()
                del self.queue[q]
    
    def appendTarget(self, target: Callable[[],None]) -> int:
        self.targets.append(target)
        return len(self.targets)
    def appendQueue(self, q: Callable[[],None], delay: int) -> int:
        self.queue.append((q, delay))
        return len(self.queue)
    def removeTarget(self, index: int) -> None:
        del self.targets[index]


class EngineQueue(Thread): # EngineQueue does not keep order, due to limitations with EngineThread
    def __init__(self, q: Callable[[], None], delay: int) -> None:
        super().__init__(target=lambda:self._call(q, delay))
    def _call(self, q: Callable[[], None], delay: int) -> None:
        time.sleep(delay)
        q()
        del self


test = Engine()
test.add(lambda:time.sleep(0.01))
test.start()
test.queue(lambda:print("1s", end=""), 1)
test.queue(lambda:print("1s", end=""), 1)
test.queue(lambda:print("1s", end=""), 1)
test.queue(lambda:print("1s", end=""), 1)
test.queue(lambda:print("1s", end=""), 1)
test.queue(lambda:print("1s"), 1)
time.sleep(2)
test.stop()
