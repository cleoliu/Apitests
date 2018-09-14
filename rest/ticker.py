import time

class ticker:
    def __init__(self, verbose=True, elapsed=False, label_only=True):
        self.verbose = verbose
        self.elapsed = elapsed
        self.label_only = label_only
        self._times = []
        self._labels = []

    def start(self, label=None):
        self._tick(label)

    def stop(self, label=None):
        self._tick(label)

    def lap(self, label=None):
        self._tick(label)

    def reset(self):
        self._times.clear()

    def _tick(self, label=None):
        self._times.append(time.time())
        self._labels.append(label)

    def print_verbose(self, elapsed=False):
        if not len(self._times):
            return
        for idx, time in enumerate(self._times):
            if idx == 0:
                base = self._times[0]
                continue

            # skip printing if there is no label
            if self.label_only and not self._labels[idx]:
                continue

            base = self._times[idx-1] if elapsed else base
            print("#{}:{} {} {} s".format(idx,
                self._labels[idx] if self._labels[idx] else '',
                "time elapsed" if elapsed else "time at",
                time - base))

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

        if self.verbose:
            self.print_verbose(self.elapsed)