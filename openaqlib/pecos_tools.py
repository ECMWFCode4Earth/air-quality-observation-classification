import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import rgb2hex

import pecos

ROOTDIR = "/Users/miha/git/esowc/air-quality-observation-classification"
RESULTSDIR = f"{ROOTDIR}/results"


def cleanup_dataframe(df, time_increment_mode):
    """replace OpenAQ missing value with np.nan and insert nans where ther are gaps"""
    start_index = df.index[0]
    end_index = df.index[-1]
    idx = pd.date_range(
        start_index, end_index, freq="{}S".format(int(time_increment_mode))
    )

    df = df.reindex(idx, fill_value=np.nan)
    # df.value.replace(-999, np.nan)
    df.value[df.value < 0] = np.nan

    return df


def get_time_increment_mode(df):

    time_diff = (df.index[1:] - df.index[:-1]).values
    mode = stats.mode(time_diff).mode[0]
    time_increment_mode = mode / np.timedelta64(1, "s")
    return time_increment_mode


def run_pecos_tests(df, location, parameter):

    pecos.logger.initialize()
    pm = pecos.monitoring.PerformanceMonitoring()

    time_increment_mode = get_time_increment_mode(df)

    df = cleanup_dataframe(df, time_increment_mode)

    no_missing_values = df.value.isna().sum()
    data_availability = (len(df.index) - no_missing_values) / len(df.index)
    print("data availabilty: ", no_missing_values, data_availability)

    pm.add_dataframe(df)

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

    # print(QCI)
    data_plot_path = f"{RESULTSDIR}/openaq_{location}_{parameter}.png"
    test_results_path = f"{RESULTSDIR}/pecos_{location}_{parameter}.png"

    test_results_graphics = pecos.graphics.plot_test_results(
        pm.df, pm.test_results, filename_root=test_results_path
    )
    # df.plot(y="value", figsize=(7.0, 3.5))
    # plt.savefig(data_plot_path, format="png", dpi=300)

    # # print(pm.test_results)

    # Report = f"{RESULTSDIR}/test_results_{location}_{parameter}.csv"
    # MonitoringReport = f"{RESULTSDIR}/MonitoringReport_{location}_{parameter}.html"

    # pecos.io.write_test_results(pm.test_results, filename=Report)
    # pecos.io.write_monitoring_report(
    #     pm.df,
    #     pm.test_results,
    #     test_results_graphics=test_results_graphics,
    #     # [data_plot_path],
    #     custom_graphics=[],
    #     metrics=QCI,
    #     filename=MonitoringReport,
    #     title="Pecos Monitoring Report",
    #     config={},
    #     logo=False,
    #     im_width_test_results=1,
    #     im_width_custom=1,
    #     im_width_logo=0.1,
    #     encode=False,
    #     file_format="html",
    # )

    plt.clf()

    return (data_availability, QCI.value)


def color_value(val):

    nThresholds = 10
    colors = [(0.75, 0.15, 0.15), (1, 0.75, 0.15), (0.15, 0.75, 0.15)]
    cmap = LinearSegmentedColormap.from_list(
        name="custom", colors=colors, N=nThresholds
    )

    # print("color val", val)
    return_color = ""
    if np.isnan(val):
        return_color = "background-color: gray"
    elif val > 1:
        return_color = "background-color: gray"
    elif val < 0:
        return_color = "background-color: gray"
    else:
        binned_value = int(np.floor(val * 10))
        rgb_color = cmap(binned_value)[:3]
        hex_color = rgb2hex(rgb_color)
        return_color = "background-color: " + hex_color

    return return_color


def generate_dashboard_cell(DA, QCI):

    metrics = pd.DataFrame(data=np.array([DA, QCI]), columns=[""], index=["DA", "QCI"])

    # Apply color and formatting to metrics table
    style_table = (
        metrics.style.format("{:.2f}")
        .applymap(color_value)
        .highlight_null(null_color="gray")
        .render()
    )

    # Store content to be displayed in the dashboard
    content = {"table": style_table}
    return content


def create_pecos_dashboard(parameter_list, location_list, dashboard_content, FILENAME):
    footnote = "DA = Data availability <br>QCI = Quality control index"

    for location in location_list:
        for parameter in parameter_list:
            if (location, parameter) not in dashboard_content:
                dashboard_content[(location, parameter)] = "&nbsp;"

    pecos.io.write_dashboard(
        parameter_list,
        location_list,
        dashboard_content,
        footnote=footnote,
        filename=FILENAME,
    )
    return
