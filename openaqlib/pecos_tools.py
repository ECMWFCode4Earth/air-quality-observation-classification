import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

import pecos

RESULTSDIR = "./results"


def get_time_increment_mode(df):

    time_diff = (df.index[1:] - df.index[:-1]).values
    mode = stats.mode(time_diff).mode[0]
    time_increment_mode = mode / np.timedelta64(1, "s")
    return time_increment_mode


def run_pecos_tests(df, location):

    pecos.logger.initialize()
    pm = pecos.monitoring.PerformanceMonitoring()

    # Step 3 Append Dataframe to Pecos PerformanceMonitoring data object
    pm.add_dataframe(df)

    time_increment_mode = get_time_increment_mode(df)
    pm.check_timestamp(time_increment_mode)

    pm.check_missing()

    stddev = df.value.std()
    mean = df.value.mean()
    lower_bound = 0
    higher_bound = mean + 5 * stddev
    pm.check_range([lower_bound, higher_bound], key="value")

    delta_lower_bound = None
    delta_higher_bound = 3 * stddev

    pm.check_delta(
        [delta_lower_bound, delta_higher_bound], window=time_increment_mode, key="value"
    )

    minimum_increment = 0.001
    pm.check_increment([minimum_increment, None], min_failures=12, key="value")

    # pm.check_outlier([None, 3], window=12 * 3600)

    # Step 9 Compute the quality control index for value
    mask = pm.mask[["value"]]
    QCI = pecos.metrics.qci(mask)

    print(QCI)
    custom = f"{RESULTSDIR}/pecos_{location}.png"

    test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
    df.plot(y="value", figsize=(7.0, 3.5))
    plt.savefig(custom, format="png", dpi=300)

    print(pm.test_results)

    Report = f"test_results_{location}.csv"

    MonitoringReport = f"{RESULTSDIR}/MonitoringReport_{location}.html"

    pecos.io.write_test_results(pm.test_results, filename=Report)
    pecos.io.write_monitoring_report(
        pm.df,
        pm.test_results,
        test_results_graphics,
        [custom],
        QCI,
        filename=MonitoringReport,
    )

    return pm.test_results

