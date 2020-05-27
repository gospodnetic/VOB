
import utilities as util

import matplotlib.pyplot as plt
import numpy as np

class Vis:
    def set_logs(self, log_container):
        self.log_container = log_container
        self.figures = []

    def generate_graphs(self):
        for approach in self.log_container.logs_per_approach:
            logs = self.log_container.logs_per_approach[approach]

            fig = plt.figure()
            ax = fig.add_subplot(111)
            per_method_coverage = []
            for log in logs:
                per_method_coverage.append(
                    util.convert_to_percentage(
                        log.get_cumulative_coverage_per_vp()))
                y = np.array(per_method_coverage[-1])
                x = np.array(range(len(y)))
                ax.plot(x, y, c="0.4", alpha=0.2)

            ax.set_xlim(0,45)
            ax.set_ylim(0,100)

            ax.set_xlabel("Number of viewpoints")
            ax.set_ylabel("Coverage [%]")
            fig.suptitle(approach)

            peaks, troughs = self.__stacked_coverage_find_peaks_and_troughs(per_method_coverage)
            peaks = self.__filter_falling_peaks(peaks)

            # plt.plot(peaks, c="#009e28", ls="--", lw=2, alpha=0.5)
            ax.plot(peaks, c="blue", ls="--", lw=2, alpha=0.5)
            ax.plot(troughs, c="#e36120", ls="--", lw=2, alpha=0.7)

            self.figures.append(fig)

    # It will show all currently created figures.
    def show_graphs(self):
        plt.show()

    def save_graphs(self, prefix="", output_path=""):
        for idx, figure in enumerate(self.figures):
            label = figure._suptitle.get_text()
            figure.suptitle("")
            if prefix != "":
                filename = output_path + prefix + "-" + label
            else:
                filename = output_path + label
            figure.savefig(filename)

    # Stacked coverages are of different lengths, pad shorter ones by
    # repeating the last value.
    def __pad_to_matrix(self, stacked_coverage):
        max_length = 0
        for row in stacked_coverage:
            if len(row) > max_length:
                max_length = len(row)

        matrix_stacked_coverage = []
        for row in stacked_coverage:
            if len(row) < max_length:
                length_difference = max_length - len(row)
                padding = np.full(length_difference, row[-1])
                row = np.concatenate([row,padding])
            matrix_stacked_coverage.append(row)

        return matrix_stacked_coverage


    # For each viewpoint ste, find maximal value from 2D data representing
    # stacked multiple coverage arrays (coverage per VP contribution of multiple methods)
    def __stacked_coverage_find_peaks_and_troughs(self, stacked_coverage):
        plot_min_padded_to_max_length = True

        # Find method with the most viewpoints (length of coverage vector = viewpoint count)
        max_length = 0
        min_length = len(stacked_coverage[0])
        for row in stacked_coverage:
            if len(row) > max_length:
                max_length = len(row)
            if len(row) < min_length:
                min_length = len(row)

        if plot_min_padded_to_max_length:
            stacked_coverage = self.__pad_to_matrix(stacked_coverage)

        peaks = []
        troughs = []
        for i in range(max_length):
            max_val = 0
            min_val = 100
            for row in stacked_coverage:
                # Check if there are enough elements.
                if len(row) <= i:
                    continue

                if row[i] > max_val:
                    max_val = row[i]
                if row[i] < min_val:
                    min_val = row[i]

            peaks.append(max_val)
            if plot_min_padded_to_max_length:
                troughs.append(min_val)
            elif i < min_length:
                troughs.append(min_val)
            # Plots minimum curve using all the coverages.
            # else:
            #     troughs.append(troughs[-1])

        return peaks,troughs

    # Cumulative values can not fall, and falling peaks will appear if some methods
    # have more viewpoints than the others
    def __filter_falling_peaks(self, peaks):
        for i in range(1,len(peaks)):
            if peaks[i] < peaks[i-1]:
                peaks[i] = peaks[i-1]
        return peaks
