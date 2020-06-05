import Log
import pprint
from enum import Enum

class LogContainer:
    def __init__(self, methods_per_approach):
        self.logs = []
        self.logs_per_approach = {}

        # Enabling searching by both method and approach with brute force implementation.
        # TODO: Bidirectional dictionary would be better for this.
        self.methods_per_approach = methods_per_approach
        self.approaches_per_method = set()

        self.__parse_methods_per_approach()

    def add_log(self, log):
        method = log.VPC["method"]
        if method in self.approaches_per_method:
            approach = self.approaches_per_method[method]
        else:
            raise Exception("Error: method '{}' has not been specified and is not known which approach does it belong to.".format(method))

        if approach in self.logs_per_approach:
            self.logs_per_approach[approach].append(log)
        else:
            self.logs_per_approach[approach] = [log]

    def print_status(self):
        for approach in self.logs_per_approach:
            print("Approach '{}' has {} logs".format(approach, len(self.logs_per_approach[approach])))

    def print_methods_per_approach(self):
        pp = pprint.PrettyPrinter(indent=4)
        print("Methods per approach:")
        pp.pprint (self.methods_per_approach)

    def get_logs_by_method(self, method):
        approach = self.approaches_per_method[method]
        if approach not in self.logs_per_approach:
            return []

        method_logs = []
        for log in self.logs_per_approach[approach]:
            if log.VPC["method"] == method:
                method_logs.append(log)

        return method_logs

    # Log which obtains coverage over 99% with minimal number of viewpoint candidates
    # If no log obrains coverage over 99%, the log with the greatest coverage is considered.
    def get_best_log(self, method):
        method_logs = self.get_logs_by_method(method)
        if len(method_logs) == 0:
            raise Exception("Error: No logs available for given method ({})".format(method))

        # Find logs with coverage >99%.
        high_coverage_logs = self.__filter_coverage_threshold(method_logs, 0.99, ComparisonType.GEQ)

        if len(high_coverage_logs) > 0:
            return self.max_coverage_log(high_coverage_logs)
        else:
            return self.max_coverage_log(method_logs)

    def max_coverage_log(self, input_logs=None):
        if not input_logs:
            input_logs = self.logs
        if len(input_logs) == 0:
            raise Exception("Error: no logs available.")

        max_coverage = input_logs[0].coverage["percent_fraction"]
        max_log = input_logs[0]
        for log in input_logs:
            if log.coverage["percent_fraction"] > max_coverage:
                max_log = log
        return max_log

    def __parse_methods_per_approach(self):
        self.approaches_per_method = {}
        for approach in self.methods_per_approach:
            for method in self.methods_per_approach[approach]:
                self.approaches_per_method[method] = approach

    # Find logs which have coverage greater or equal to the given threshold.
    # threshold is given as a fraction (e.g. 0.99)
    def __filter_coverage_threshold(self, input_logs, threshold, comparison_type):
        filtered_logs = []
        for log in input_logs:
            if comparison_type == ComparisonType.G:
                if log.coverage["percent_fraction"] > threshold:
                    filtered_logs.append(log)
            elif comparison_type == ComparisonType.GEQ:
                if log.coverage["percent_fraction"] >= threshold:
                    filtered_logs.append(log)
            elif comparison_type == ComparisonType.LEQ:
                if log.coverage["percent_fraction"] <= threshold:
                    filtered_logs.append(log)
            elif comparison_type == ComparisonType.L:
                if log.coverage["percent_fraction"] < threshold:
                    filtered_logs.append(log)

        return filtered_logs

class ComparisonType(Enum):
    G = 0       # >
    GEQ = 1     # >=
    LEQ = 2     # <=
    L = 3       # <
