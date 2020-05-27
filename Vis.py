
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
            for log in logs:
                per_method_coverage = []
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

