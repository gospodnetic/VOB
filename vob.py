from Log import Log

import sys
import json

def main():
    if (len(sys.argv) == 2):
        path_list = sys.argv[1]
    else:
        print("No .json file containing OVP paths provided.")
        exit()

    with open(path_list) as ovp_path_file:
        ovp_paths = json.load(ovp_path_file)

    for filename in ovp_paths:
        log = Log(filename)
        print(log)

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
