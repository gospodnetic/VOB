import Log
import pprint

class LogContainer:
    def __init__(self, methods_per_approach):
        self.logs = []
        self.logs_per_approach = {}

        # Enabling searching by both method and approach with brute force implementation.
        # TODO: Bidirectional dictionary would be better for this.
        self.methods_per_approach = methods_per_approach
        self.approaches_per_method = {}

        self.__parse_methods_per_approach()

    def __parse_methods_per_approach(self):
        self.approaches_per_method = {}
        for approach in self.methods_per_approach:
            for method in self.methods_per_approach[approach]:
                self.approaches_per_method[method] = approach

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

    def print_methods_per_approache(self):
        pp = pprint.PrettyPrinter(indent=4)
        print("Methods per approach:")
        pp.pprint (self.methods_per_approach)
