
from Benchmark import Benchmark
from Log import Log
from LogContainer import LogContainer
from Vis import Vis

import os
import pathlib
import sys
import json

def filter_json(filenames):
    return list(filter(lambda x: pathlib.Path(x).suffix == '.json', filenames))

def extract_json_filenames(json_list):
    ovp_filenames = []
    for path in json_list:
        if os.path.isdir(path):
            for (dirpath, dirnames, filenames) in os.walk(path):
                ovp_filenames.extend(list(map(lambda x: dirpath + "/" + x, filenames)))
                break
        else:
            ovp_filenames.append(path)
    return filter_json(ovp_filenames)

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

    filenames = extract_json_filenames(ovp_paths)

    # Load log files and sort them per model.
    log_container_per_model = {}
    logs = []
    for idx, filename in enumerate(filenames):
        print("Loading file {}/{}        ".format(idx+1, len(filenames)), end="\r")
        # VP-Tri maps are big and take long to load, only to see there is nothing there.
        # Currently the maps can be only distinguished by having this string in the filename.
        if "VP-Tri_Map" in filename:
            continue

        try:
            log = Log(filename)
            logs.append(log)
        except Exception as e:
            # TODO add verbose
            # print("Error: {}\nSkipping file".format(e))
            continue

        model_name = log.model["name"]
        if model_name not in log_container_per_model:
            log_container_per_model[model_name] = LogContainer(methods_per_approach)

        try:
            log_container_per_model[model_name].add_log(log)
        except Exception as e:
            # print("Error: {}\nSkipping file".format(e))
            continue
    print("Loaded {} log files.".format(len(logs)))

    # Generate per-approach coverage graphs for each model
    vis = Vis()
    for model in log_container_per_model:
        print("Model name: {}".format(model))
        log_container_per_model[model].print_status()
        vis.set_logs(log_container_per_model[model])
        vis.generate_graphs()
        vis.save_graphs(prefix=model, output_path="./data/")
        # vis.show_graphs()

    benchmark = Benchmark()
    benchmark.set_log_containers(log_container_per_model)
    benchmark.generate_performance_tex_table()
    benchmark.generate_complete_tex_table()
    benchmark.get_average_RT_duration_per_model()
    benchmark.get_average_discarded_per_approach()
    benchmark.get_average_discarded_per_model()
    benchmark.get_average_discarded_per_model_per_approach()


if __name__ == "__main__":
    main()
