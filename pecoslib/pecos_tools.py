import numpy as np
from scipy import stats

import pecos


def get_time_increment(df):

    time_diff = (df.index[1:] - df.index[:-1]).values
    mode = stats.mode(time_diff).mode[0]
    mode_s = mode / np.timedelta64(1, "s")


def get_acceptable_range(df, sigma=5):

    df.value


def run_pecos_tests(df):

    pecos.logger.initialize()
    pm = pecos.monitoring.PerformanceMonitoring()

    # Step 3 Append Dataframe to Pecos PerformanceMonitoring data object
    pm.add_dataframe(df)

    time_increment = get_time_increment(df)

    pm.check_timestamp(time_increment)

    # Step 5 Check for missing data
    pm.check_missing()

    # Step 6 Choose acceptable value range and Check data for expected ranges
    #
    # Parameters
    #
    #  1 Lower bound of values
    #  2 Higher Bound of values
    #  3 Data column (default = None, which indicates that all columns are used)
    #  4 Minimum number of consecutive failures for reporting (default = 1)le increment from measurements of 15 minutes and check for abrupt changes between consecutive time steps
    #
    #   e.g pm.check_range([0, 200], key='value')
    #         pm.check_range([1, 2], key='3',4)
    #
    # Results: Any value outside of the range is an outlier

    LowerBound = None  # Edit

    HigherBound = 200  # Edit

    pm.check_range([LowerBound, HigherBound], key="value")

    # Step 7 Choose the min amount that is acceptable to change from measurements
    #
    # Parameters:
    #
    #    1 Lower bound to decrease by
    #    2 Upper bound to increase by
    #    3 Size of the moving window used to compute the difference between the minimum and maximum
    #    4 Data column (default = None, which indicates that all columns are used)
    #    5 Flag indicating if the test should only check for positive delta (the min occurs before the max) or negative delta (the max occurs before the min) (default = False)
    #    6 Minimum number of consecutive failures for reporting (default = 1)

    #  e.g. pm.check_delta([Miniumn Decrease, Min Increase], window=3600, 'value')
    #      included parametes 1-6: pm.check_delta([1, 2], window=3, key='4', 5, 6)
    #
    #  Results: When over min decrease or increase it is an outlier

    print("*****")

    print("Criteria 3 : Stagnant Measurements ")

    DeltaLowerBound = None  # Edit

    DeltaHigherBound = 10  # Edit

    DeltaTimeSchedule = 3600  # Edit

    pm.check_delta(
        [DeltaLowerBound, DeltaHigherBound], window=DeltaTimeSchedule, key="value"
    )

    print(" Measurement that increase by ")

    print(DeltaHigherBound)

    print("in Time Schedule")

    print(DeltaTimeSchedule)

    print("Delta Lower Bound")

    print(DeltaLowerBound)
    # Step 8 Choose acceptable increment on measurements
    #
    # Parameters
    #
    #  1 Lower bound to de increment by
    #  2 Higher Bound to increment by
    #  3 Data column (default = None, which indicates that all columns are used)
    #  4 Increment used for difference calculation (default = 1 timestamp)
    #  5 Flag indicating if the absolute value of the increment is used in the test (default = True)
    #  6 Minimum number of consecutive failures for reporting (default = 1)
    #
    # e.g pm.check_increment([None, 20], 'value')
    #    included parametes 1- 4:  pm.check_increment([1, 2], key='3', 4, 5, 6)
    #
    # Results: Any measurement that has a larger increment or de increment by choosen value is an outlier

    print("*****")

    print("Criteria 3 : Stagnant Measurements ")

    Increment_Increase = 20  # Edit

    Increment_Decrease = None  # Edit

    pm.check_increment([None, 20], key="value")

    print("Increment Increase")

    print(Increment_Increase)

    print("Increment Decrease")

    print(Increment_Decrease)

    pm.check_outlier([None, 3], window=12 * 3600)

    # Step 9 Compute the quality control index for value
    mask = pm.mask[["value"]]
    QCI = pecos.metrics.qci(mask)

    print("*****")

    print("OpenAQ Dataset Results ")

    print("Mask")

    print(mask)

    print("Performance Metrics")

    print(QCI)

    custom = "custom" + iteration_OpenAQStations + ".png"

    MeasurementOpenAQ = int(OpenAQStation["value"].max())

    print(OpenAQStation["value"].describe())

    # Step 10 Generate graphics
    test_results_graphics = pecos.graphics.plot_test_results(pm.df, pm.test_results)
    OpenAQStation.plot(y="value", ylim=[0, MeasurementOpenAQ], figsize=(7.0, 3.5))
    plt.savefig(custom, format="png", dpi=500)

    print(pm.test_results)

    # Step 11 Write test results and report files to test_results.csv and monitoringreport.html

    Report = "test_results" + OpenAQStation_Dataset + iteration_OpenAQStations + ".csv"

    MonitoringReport = (
        "MonitoringReport" + OpenAQStation_Dataset + iteration_OpenAQStations + ".html"
    )

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

