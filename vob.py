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
        print("arg1 - methods_per_approach.json\narg2 - path_list\n[arg3] - graphs filename prefix")
        exit()

    with open(path_list) as ovp_path_file:
        ovp_paths = json.load(ovp_path_file)
    with open(methods_per_approach_filename) as methods_per_approach_file:
        methods_per_approach = json.load(methods_per_approach_file)

    # Load log files and sort them per model.
    log_containers_per_model = {}
    logs = []
    for filename in ovp_paths:
        log = Log(filename)
        try:
            logs.append(log)
        except Exception as e:
            print("Error: {}\nSkipping file".format(e))
            continue

        model_name = log.model["name"]
        if model_name not in log_containers_per_model:
            print(model_name)
            log_containers_per_model[model_name] = LogContainer(methods_per_approach)

        try:
            log_containers_per_model[model_name].add_log(log)
        except Exception as e:
            print("Error: {}\nSkipping file".format(e))
            continue
    print("Loaded {} log files.".format(len(logs)))

    # Generate per-approach coverage graphs for each model
    vis = Vis()
    for model in log_containers_per_model:
        print("Model name: {}".format(model))
        log_containers_per_model[model].print_status()
        vis.set_logs(log_containers_per_model[model])
        vis.generate_graphs()
        vis.save_graphs(prefix=model, output_path="./data/")
        # vis.show_graphs()


if __name__ == "__main__":
    main()
