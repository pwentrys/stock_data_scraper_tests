from time import time
from typing import Tuple


class Timings:
    """

    """
    SLEEP_TIME = 2
    ESTIMATE_MULTI = 1.15

    def __init__(self):
        self._start = 0.0
        self._stop = 0.0
        self._stop_estimate = 0.0
        self._duration_actual = 0.0
        self._duration_estimate = 0.0
        self._duration_error = 0.0
        self._op_its = 0  # operation iterations
        self._counter = 0  # count which op we're at.

    def start(self):
        """
        Start timer.
        :return:
        """
        self._counter, self._start, self._stop_estimate = Timings._calculate_stop_estimate(time(),
                                                                                           self._duration_estimate)

    @staticmethod
    def _calculate_stop_estimate(start: float, duration: float) -> Tuple[int, float, float]:
        """
        Calculate stop estimates.
        :param start:
        :param duration:
        :return:
        """
        return 0, start, start + duration

    def start_logged(self):
        """
        Run start and return log print.
        :return:
        """
        self.start()
        print('\n'.join([
            f'Start Time: {self._start}',
            f'Est Run: {self._duration_estimate}',
            f'Est Stop: {self._stop_estimate}',
            f'Op Its: {self._op_its}'
        ]))

    def stop(self):
        """
        Stop timer.
        :return:
        """
        self._stop, self._duration_actual, self._duration_error = Timings._calculate_duration(self._start, time(),
                                                                                              self._duration_estimate)

    def stop_logged(self):
        """
        Run stop and return log print.
        :return:
        """
        self.stop()
        print('\n'.join([
            f' ---- Times  ---- ',
            f'Started: {self._start}',
            f'Finished: {self._stop}',
            f'Estimated: {self._stop_estimate}',
            f' ----- Run  ----- ',
            f'Actual: {self._duration_actual}',
            f'Estimated: {self._duration_estimate}',
            f'Error: {self._duration_error}',
            f' ---------------- '
        ]))

    @staticmethod
    def _calculate_duration_and_diff(estimate: float, actual: float) -> Tuple[float, float]:
        """
        Calculate duration and errors.
        :param estimate:
        :param actual:
        :return:
        """
        return actual, (estimate - actual) if estimate > actual else (actual - estimate)

    @staticmethod
    def _calculate_duration(start: float, stop: float, estimate: float) -> Tuple[float, float, float]:
        """
        Get duration and errors calculated.
        :param start:
        :param stop:
        :param estimate:
        :return:
        """
        duration, difference = Timings._calculate_duration_and_diff(estimate, stop - start)
        return stop, duration, difference

    @staticmethod
    def _estimate_duration(op_its: int, offset_multi: float) -> Tuple[float, float]:
        """
        Calculate run time estimate.

        (Operations x Iterations) x (Sleep Time x Offset Multi)
        :param op_its:
        :param offset_multi:
        :return:
        """
        return op_its, op_its * offset_multi

    def estimate_duration(self, operations: int, iterations: int):
        """
        Get run time estimate.
        :param operations:
        :param iterations:
        :return:
        """
        self._op_its, self._duration_estimate = Timings._estimate_duration(operations * iterations,
                                                                           self.SLEEP_TIME * self.ESTIMATE_MULTI)

    @staticmethod
    def _operation_logged(counter: int, total: int, start: float) -> int:
        """
        Print log and return incremented counter.
        :param counter:
        :param total:
        :param start:
        :return:
        """
        print(f'{counter} / {total}     -     Elapsed: {time() - start}')
        return counter

    def operation_logged(self):
        """
        Increment counter and log progress.
        :return:
        """
        self._counter = Timings._operation_logged(self._counter + 1, self._op_its, self._start)
