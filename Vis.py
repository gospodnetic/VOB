
import utilities as util

import matplotlib.pyplot as plt
import numpy as np

class Vis:
    def set_logs(self, log_container):
        self.log_container = log_container

    def generate_graphs(self):
        for approach in self.log_container.logs_per_approach:
            logs = self.log_container.logs_per_approach[approach]

            plt.figure(num=approach)
            for log in logs:
                per_method_coverage = []
                per_method_coverage.append(
                    util.convert_to_percentage(
                        log.get_cumulative_coverage_per_vp()))
                y = np.array(per_method_coverage[-1])
                x = np.array(range(len(y)))
                plt.plot(x, y, c="0.4", alpha=0.2)

            plt.xlim(0,45)
            plt.ylim(0,100)

            plt.xlabel("Number of viewpoints")
            plt.ylabel("Coverage [%]")
        plt.show()
