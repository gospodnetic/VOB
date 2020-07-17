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

    def generate_statistic_tex(self, output_path = "./"):
        # Per model per method.
        filename = output_path + "stats_per_method.tex"
        tex_file = open(filename, "w")

        tex_file.write("\n\\begin{table*}\n")
        tex_file.write("\\centering\n")
        tex_file.write("\\begin{tabular}{|c|")
        tex_file.write(" c|" * len(self.log_container_per_model))
        tex_file.write("}\n")
        tex_file.write("\\hline\n")

        discarded_per_method = self.get_average_discarded_per_method()
        discarded_per_model_per_method = self.get_average_discarded_per_model_per_method()

        # Write header.
        tex_file.write(" ")
        for model in self.log_container_per_model:
            tex_file.write(" & {}".format(model))
        tex_file.write("\\\\\n")

        for method in discarded_per_method:
            #  Average value over all models.
            tex_file.write("\n\\hline\n")
            tex_file.write("\\multirow{{{}}}{{*}}{{\\makecell{{{}}}}}".format(2, method))
            value = util.set_precision(discarded_per_method[method] * 100, 2)
            tex_file.write("\n& \\multicolumn{{4}}{{c|}}{{{}}}".format(value))
            tex_file.write("\\\\\n")
            # Draw horizontal line spanning only under the multicolumn section.
            tex_file.write("\n\\cline{{2-{}}}\n".format(len(self.log_container_per_model) + 1))
            # Average value for each model.
            for model in discarded_per_model_per_method:
                value = util.set_precision(discarded_per_model_per_method[model][method] * 100, 2)
                tex_file.write(" & \\makecell{{{}}}".format(value))
            tex_file.write("\\\\\n")
        
        tex_file.write("\n\\hline\n")
        tex_file.write("\\end{tabular}")
        tex_file.write("\n\\end{table*}\n")
        tex_file.close()

        # Per model per approach.
        filename = output_path + "stats_per_approach.tex"
        tex_file = open(filename, "w")

        tex_file.write("\n\\begin{table*}\n")
        tex_file.write("\\centering\n")
        tex_file.write("\\begin{tabular}{|c|")
        tex_file.write(" c|" * len(self.log_container_per_model))
        tex_file.write("}\n")
        tex_file.write("\\hline\n")

        discarded_per_approach = self.get_average_discarded_per_approach()
        discarded_per_model_per_approach = self.get_average_discarded_per_model_per_approach()

        # Write header.
        tex_file.write(" ")
        for model in self.log_container_per_model:
            tex_file.write(" & {}".format(model))
        tex_file.write("\\\\\n")

        for approach in discarded_per_approach:
            print(approach)
            #  Average value over all models.
            tex_file.write("\n\\hline\n")
            tex_file.write("\\multirow{{{}}}{{*}}{{\\makecell{{{}}}}}".format(2, approach))
            value = util.set_precision(discarded_per_approach[approach] * 100, 2)
            tex_file.write("\n& \\multicolumn{{4}}{{c|}}{{{}}}".format(value))
            tex_file.write("\\\\\n")
            # Draw horizontal line spanning only under the multicolumn section.
            tex_file.write("\n\\cline{{2-{}}}\n".format(len(self.log_container_per_model) + 1))
            # Average value for each model.
            for model in discarded_per_model_per_approach:
                value = util.set_precision(discarded_per_model_per_approach[model][approach] * 100, 2)
                tex_file.write(" & \\makecell{{{}}}".format(value))
            tex_file.write("\\\\\n")
        
        tex_file.write("\n\\hline\n")
        tex_file.write("\\end{tabular}")
        tex_file.write("\n\\end{table*}\n")
        tex_file.close()



    # \usepackage{makecell} needed.
    # \usepackage{multirow} needed.
    def generate_performance_tex_table(self, output_path = "./", coverage_threshold=0.99, with_discarded=True):
        filename = output_path
        if with_discarded:
            filename += "performance_table_discarded.tex"
        else:
            filename += "performance_table.tex"
        tex_file = open(filename, "w")

        tex_file.write("\n\\begin{table*}\n")
        tex_file.write("\\centering\n")
        tex_file.write("\\begin{tabular}{|c| c|")
        for model in self.log_container_per_model:
            if with_discarded:
                tex_file.write(" c c c c|")
            else:
                tex_file.write(" c c c|")
        tex_file.write("}\n")
        tex_file.write("\\hline\n")

        # Header - model names
        tex_file.write("\\multicolumn{2}{|c|}{}")

        # Put models into array to ensure the order is always maintained.
        models = []
        if with_discarded:
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
                            best_log = self.log_container_per_model[model].get_best_log(method, coverage_threshold)
                        except Exception as e:
                            tex_file.write(" & - & - & - & -")
                            continue

                        VPC_count = best_log.VPC["count"] + best_log.VPC["discarded_count"]
                        VPC_used = best_log.VPC["count"]
                        OVP = len(best_log.optimization["OVP"])
                        coverage = util.set_precision(best_log.coverage["percent_fraction"] * 100, 2)
                        tex_file.write(" & {} & {} & {} & {}".format(VPC_count, VPC_used, OVP, coverage))
                    tex_file.write("\\\\")
        else:
            for model in self.log_container_per_model:
                tex_file.write(" & \\multicolumn{{3}}{{|c|}}{{{}}}".format(model))
                models.append(model)
            tex_file.write("\\\\\n")
            
            # Header - column names
            tex_file.write("\\hline\n")
            tex_file.write("Approach & Method")
            for model in models:
                tex_file.write(" & \\#VPC & \\#OVP & \\%")
            tex_file.write("\\\\\n")


            for approach in self.methods_per_approach:
                method_count = len(self.methods_per_approach[approach])
                tex_file.write("\n\\hline\n")
                tex_file.write("\\multirow{{{}}}{{*}}{{\\makecell{{{}}}}}".format(method_count, approach))

                for method in self.methods_per_approach[approach]:
                    tex_file.write("\n& \makecell{{{}}}".format(method))

                    for model in models:
                        try:
                            best_log = self.log_container_per_model[model].get_best_log(method, coverage_threshold)
                        except Exception as e:
                            tex_file.write(" & - & - & -")
                            continue

                        VPC_count = best_log.VPC["count"] + best_log.VPC["discarded_count"]
                        OVP = len(best_log.optimization["OVP"])
                        coverage = util.set_precision(best_log.coverage["percent_fraction"] * 100, 2)
                        tex_file.write(" & {} & {} & {}".format(VPC_count, OVP, coverage))
                    tex_file.write("\\\\")

        tex_file.write("\n\\hline\n")
        tex_file.write("\\end{tabular}")
        tex_file.write("\n\\end{table*}\n")
        tex_file.close()

    # \usepackage{longtable} needed.
    def generate_complete_tex_table(self, output_path = "./"):
        tex_file = open(output_path + "complete_table.tex", "w")

        for model in self.log_container_per_model:
            tex_file.write("\n\\begin{longtable}{|c c c c c c c c|}\n")
            tex_file.write("\\hline\n")
            if self.log_container_per_model[model].size() == 0:
                raise Exception("Model log container of size 0, Object space exploration approach method likely not specified!")

            first_log = self.log_container_per_model[model].logs[0]
            tex_file.write("\\multicolumn{{8}}{{|c|}}{{{} ({})}}\\\\\n".format(model, first_log.model["face_count"]))
            tex_file.write("Method & Parameter & \\#VPC & \\#Discarded & \\#OVP & RT[S] & NBV[s] & coverage \\\\\n")
            for approach in self.methods_per_approach:
                for method in self.methods_per_approach[approach]:
                    logs_per_method = self.log_container_per_model[model].get_logs_by_method(method)
                    if len(logs_per_method) == 0:
                        continue

                    for log in logs_per_method:
                        tex_file.write("{} & {} & {} & {} & {} & {} & {} & {} \\\\\n".format(
                            log.VPC["method"],
                            log.VPC["generation_parameter"],
                            log.VPC["count"] + log.VPC["discarded_count"],
                            log.VPC["discarded_count"],
                            len(log.optimization["OVP"]),
                            util.set_precision(log.timing["visibility_matrix_sec"], 4),
                            util.set_precision(log.timing["optimization_sec"], 4),
                            util.set_precision(log.coverage["percent_fraction"], 4)))
            tex_file.write("\\hline\n")
            tex_file.write("\\end{longtable}\n")

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

        return discarded_per_approach

    def get_average_discarded_per_method(self):
        discarded_per_method_list = {}
        for approach in self.methods_per_approach:
            for method in self.methods_per_approach[approach]:
                for model in self.log_container_per_model:
                    log_container = LogContainer(self.log_container_per_model[model].get_methods_per_approach())
                    log_container.add_logs(self.log_container_per_model[model].get_logs_by_method(method))
                    if log_container.size() == 0:
                        continue

                    container_avg = log_container.get_avg_discarded()
                    if method in discarded_per_method_list:
                        discarded_per_method_list[method].append(container_avg)
                    else:
                        discarded_per_method_list[method] = [container_avg]
        discarded_per_method = {}
        for method in discarded_per_method_list:
            discarded_per_method[method] = np.sum(discarded_per_method_list[method]) / len(discarded_per_method_list[method])

        return discarded_per_method

    def get_average_discarded_per_model(self):
        discarded_per_model = {}
        for model in self.log_container_per_model:
            model_avg = self.log_container_per_model[model].get_avg_discarded()
            discarded_per_model[model] = model_avg
        print("discarded_per_model {}".format(discarded_per_model))
        return discarded_per_model

    def get_average_discarded_per_model_per_method(self):
        discarded_per_model_method = {}
        for model in self.log_container_per_model:
            for approach in self.methods_per_approach:
                for method in self.methods_per_approach[approach]:
                    log_container = LogContainer(self.log_container_per_model[model].get_methods_per_approach())
                    log_container.add_logs(self.log_container_per_model[model].get_logs_by_method(method))
                    if log_container.size() == 0:
                        continue
                    if model in discarded_per_model_method:
                        discarded_per_model_method[model][method] = log_container.get_avg_discarded()
                    else:
                        discarded_per_model_method[model] = {}
                        discarded_per_model_method[model][method] = log_container.get_avg_discarded()

        return discarded_per_model_method

    def get_average_discarded_per_model_per_approach(self):
        discarded_per_model_approach = {}
        for model in self.log_container_per_model:
            for approach in self.methods_per_approach:
                log_container = LogContainer(self.log_container_per_model[model].get_methods_per_approach())
                log_container.add_logs(self.log_container_per_model[model].get_logs_by_approach(approach))
                if log_container.size() == 0:
                    continue
                if model in discarded_per_model_approach:
                    discarded_per_model_approach[model][approach] = log_container.get_avg_discarded()
                else:
                    discarded_per_model_approach[model] = {}
                    discarded_per_model_approach[model][approach] = log_container.get_avg_discarded()

        return discarded_per_model_approach
