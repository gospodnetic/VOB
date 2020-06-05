
import utilities as util
from LogContainer import LogContainer

import numpy as np

class Benchmark:
    def __init__(self):
        self.log_container_per_model = {}
        self.methods_per_approach = {}

    def set_log_containers(self, log_container_per_model):
        self.log_container_per_model = log_container_per_model
        self.__extract_methods_per_approach()

    def __extract_methods_per_approach(self):
        for model in self.log_container_per_model:
            for approach in self.log_container_per_model[model].methods_per_approach:
                for method in self.log_container_per_model[model].methods_per_approach[approach]:
                    if approach in self.methods_per_approach:
                        if method not in self.methods_per_approach[approach]:
                            self.methods_per_approach[approach].append(method)
                    else:
                        self.methods_per_approach[approach] = [method]

    def generate_tex_table(self):
        tex_file = open("performance_table.tex", "w")

        tex_file.write("\n\\begin{table*}\n")
        tex_file.write("\\begin{tabular}{|c| c|")
        for model in self.log_container_per_model:
            tex_file.write(" c c c c|")
        tex_file.write("}\n")
        tex_file.write("\\hline\n")

        # Header - model names
        tex_file.write("\\multicolumn{2}{|c|}{}")

        # Put models into array to ensure the order is always maintained.
        models = []
        for model in self.log_container_per_model:
            tex_file.write(" & \\multicolumn{{4}}{{|c|}}{{{}}}".format(model))
            models.append(model)
        tex_file.write("\\\\\n")
        
        # Header - column names
        tex_file.write("\\hline\n")
        tex_file.write("Approach & Method")
        for model in models:
            tex_file.write(" & \\#VPC & \\makecell{\\#VPC\\\\used} & \\#OVP & \\%")
        tex_file.write("\\\\\n")


        for approach in self.methods_per_approach:
            method_count = len(self.methods_per_approach[approach])
            tex_file.write("\n\\hline\n")
            tex_file.write("\\multirow{{{}}}{{*}}{{\\makecell{{{}}}}}".format(method_count, approach))

            for method in self.methods_per_approach[approach]:
                tex_file.write("\n& \makecell{{{}}}".format(method))

                for model in models:
                    try:
                        best_log = self.log_container_per_model[model].get_best_log(method)
                    except:
                        tex_file.write(" & - & - & - & -")
                        continue

                    VPC_count = best_log.VPC["count"] + best_log.VPC["discarded_count"]
                    VPC_used = best_log.VPC["count"]
                    OVP = len(best_log.optimization["OVP"])
                    coverage = util.set_precision(best_log.coverage["percent_fraction"] * 100, 2)
                    tex_file.write(" & {} & {} & {} & {}".format(VPC_count, VPC_used, OVP, coverage))
                tex_file.write("\\\\")

        tex_file.write("\n\\end{tabular}")
        tex_file.write("\n\\end{table*}\n")
        tex_file.close()

    # Average ray tracing duration.
    def get_average_RT_duration_per_model(self):
        avgs = {}
        for model in self.log_container_per_model:
            avgs.update(
            {
                model: self.log_container_per_model[model].get_avg_RT_duration()
            })
        return avgs

    def get_average_discarded_per_approach(self):
        discarded_per_approach_list = {}
        for approach in self.methods_per_approach:
            for model in self.log_container_per_model:
                log_container = LogContainer(self.log_container_per_model[model].get_methods_per_approach())
                log_container.add_logs(self.log_container_per_model[model].get_logs_by_approach(approach))
                if log_container.size() == 0:
                    continue

                container_avg = log_container.get_avg_discarded()
                if approach in discarded_per_approach_list:
                    discarded_per_approach_list[approach].append(container_avg)
                else:
                    discarded_per_approach_list[approach] = [container_avg]
        
        discarded_per_approach = {}
        for approach in discarded_per_approach_list:
            discarded_per_approach[approach] = np.sum(discarded_per_approach_list[approach]) / len(discarded_per_approach_list[approach])

        print("discarded_per_approach: {}".format(discarded_per_approach))
        return discarded_per_approach

