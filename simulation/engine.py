from threading import Thread
from collections.abc import Callable
import time


class Engine:
    """
    A simplified layer between main and _EngineThread/_EngineQueue.\n
    When passing functions with arguments use ```lambda:```.\n
    When queuing functions know functions that end at the same time
    have a tendency to change when they end at each program run.
    If a function needs to end after another, delaying the function by
    0.1 should fix the issue
    """

    def __init__(self) -> None:
        self.thread = _EngineThread()
    
    def start(self) -> None:
        self.thread.start()
    
    def stop(self) -> None:
        self.thread.stop = True
    
    def pause(self) -> None:
        self.thread.paused = not self.thread.paused
    
    def add(self, target: Callable[[],None]) -> None:
        self.thread.appendTarget(target)
    
    def remove(self, index: int) -> None:
        self.thread.removeTarget(index)
    
    def queue(self, target: Callable[[],None], delay: int|float) -> None:
        self.thread.appendQueue(target, delay)



class _EngineThread(Thread):
    def __init__(self) -> None:
        self.stop: bool = False
        self.paused: bool = False
        self.targets: list[Callable[[], None]] = []
        self.queue: list[tuple[Callable[[], None], int|float]] = []
        super().__init__(target=lambda:self._call())

    def _call(self) -> None:
        while self.stop == False:
            if self.paused:
                continue
            for t in self.targets:
                t()
            for q in range(len(self.queue)-1,-1,-1):
                tmp = _EngineQueue(self.queue[q][0], self.queue[q][1])
                tmp.start()
                del self.queue[q]

    def appendTarget(self, target: Callable[[],None]) -> int:
        self.targets.append(target)
        return len(self.targets)

    def appendQueue(self, q: Callable[[],None], delay: int|float) -> None:
        self.queue.append((q, delay))

    def removeTarget(self, index: int) -> None:
        del self.targets[index]


class _EngineQueue(Thread):
    """
    _EngineQueue is managed by Engine.

    _EngineQueue does not keep order with items executed at the same time.
    If order is neccissary adding a slight delay will aid this issue.
    """
    def __init__(self, q: Callable[[], None], delay: int|float) -> None:
        super().__init__(target=lambda:self._call(q, delay))

    def _call(self, q: Callable[[], None], delay: int|float) -> None:
        time.sleep(delay)
        q()
        del self



if __name__ == "__main__":
    test = Engine()
    test.add(lambda:print(".", end=""))
    test.add(lambda:time.sleep(0.01))
    test.start()
    test.queue(lambda:print("1s", end=""), 1)
    test.queue(lambda:print("1s", end=""), 1)
    test.queue(lambda:print("1s", end=""), 1)
    test.queue(lambda:print("1s", end=""), 1)
    test.queue(lambda:print("1s", end=""), 1)
    test.queue(lambda:print("1s"), 1.01)
    time.sleep(2)
    test.stop()
