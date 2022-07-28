from datetime import datetime
import os

from src.usecases.sar.sar_usecase import run_sar_usecase


def benchmark_func():
    run_sar_usecase()


def run_profiler_experiment():
    import cProfile
    import pstats

    func_name = "benchmark_func()"
    # prof_name = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.profile"
    prof_name = f"{datetime.now().strftime('%Y%m%d-%H%M')}.profile"

    path = os.path.join("benchmarking", "benchmarks", prof_name)

    # pr = cProfile.run(func_name, sort='tottime', filename=f"benchmarking{prof_name}.profile")
    pr = cProfile.run(func_name, sort="tottime", filename=path)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()


if __name__ == "__main__":
    run_profiler_experiment()
    # benchmark_func()