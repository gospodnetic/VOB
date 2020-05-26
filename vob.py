from Log import Log
from Vis import Vis
from LogContainer import LogContainer

import sys
import json

def main():
    if len(sys.argv) > 2:
        methods_per_approach_filename = sys.argv[1]
        path_list = sys.argv[2]
        if len(sys.argv) == 4:
            graph_filename_prefix = sys.argv[3]
    else:
        print("Error: File containing OVP paths or object exploration methods is missing.")
        exit()

    with open(path_list) as ovp_path_file:
        ovp_paths = json.load(ovp_path_file)
    with open(methods_per_approach_filename) as methods_per_approach_file:
        methods_per_approach = json.load(methods_per_approach_file)

    log_container = LogContainer(methods_per_approach)
    logs = []
    for filename in ovp_paths:
        try:
            logs.append(Log(filename))
        except Exception as e:
            print("Error: {}\nSkipping file".format(e))
            continue
        try:
            log_container.add_log(Log(filename))
        except Exception as e:
            print("Error: {}\nSkipping file".format(e))
            continue

    print("Loaded {} log files.".format(len(logs)))
    log_container.print_status()
    vis = Vis()
    vis.set_logs(log_container)

if __name__ == "__main__":
    main()

    # per_method_coverage = []
    # for filename in ovp_paths:
    #     with open(filename) as OVP_file:
    #         ovp_data = json.load(OVP_file)

    #     if ovp_data["Log"]["CoveragePerVP"] is None:
    #         print("No coverage")
    #         continue

    #     per_method_coverage.append(
    #         convert_to_percentage(
    #             convert_cumulative(np.array(ovp_data["Log"]["CoveragePerVP"]))))
    #     y = np.array(per_method_coverage[-1])
    #     x = np.array(range(len(y)))
    #     plt.plot(x, y, c="0.4", alpha=0.2)

    # peaks, troughs = stacked_coverage_find_peaks_and_troughs(per_method_coverage)
    # peaks = filter_falling_peaks(peaks)

    # # plt.plot(peaks, c="#009e28", ls="--", lw=2, alpha=0.5)
    # plt.plot(peaks, c="blue", ls="--", lw=2, alpha=0.5)
    # plt.plot(troughs, c="#e36120", ls="--", lw=2, alpha=0.7)

    # plt.xlim(0,45)
    # plt.ylim(0,100)

    # plt.xlabel("Number of viewpoints")
    # plt.ylabel("Coverage [%]")
    # # plt.show()
    # plt.savefig(graph_name)
