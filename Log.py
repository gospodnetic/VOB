
import json

import sys

class Log:
    def __init__(self, log_filename):
        self.camera_parameters = {
            "focusing_distance_mm": 0,
            "focal_length": 0,
            "model": "",
            "pixel_size_mm": 0,
            "height": 0,
            "width": 0
        }

        self.coverage = {
            "triangle_count": 0,
            "percent_fraction": 0
        }

        self.timing = {
            "visibility_matrix_sec": 0,
            "optimization_sec": 0
        }

        self.model = {
            "name": 0,
            "face_count": 0,
            "vertex_count": 0
        }

        self.VPC = {
            "count": 0,
            "discarded_count": 0,
            "method": "",
            "generation_parameter": 0
        }

        self.optimization = {
            "type": "",
            "coverage_per_vp": [],
            "triangle_per_vp": [],
            "vp_selection_order": [],
            "OVP": []
        }

        self.__parse_filename(log_filename)

    def __str__(self):
        return """
            Camera:
                focusing_distance_mm: {}
                focal_length: {}
                model: {}
                pixel_size_mm: {}
                height: {}
                width: {}
            Coverage:
                triangle_count: {}
                percent_fraction: {}
            Timing:
                visibility_matrix_sec: {}
                optimization_sec: {}
            Model:
                name: {}
                face_count: {}
                vertex_count: {}
            VPC:
                count: {}
                discarded_count: {}
                method: {}
                generation_parameter: {}
            Optimization:
                type: {}
                coverage_per_vp: _list_length_{}
                triangle_per_vp: _list_length_{}
                vp_selection_order: _list_length_{}
                OVP: _list_length_{}
            """.format(
                    self.camera_parameters["focusing_distance_mm"],
                    self.camera_parameters["focal_length"],
                    self.camera_parameters["model"],
                    self.camera_parameters["pixel_size_mm"],
                    self.camera_parameters["height"],
                    self.camera_parameters["width"],
                    self.coverage["triangle_count"],
                    self.coverage["percent_fraction"],
                    self.timing["visibility_matrix_sec"],
                    self.timing["optimization_sec"],
                    self.model["name"],
                    self.model["face_count"],
                    self.model["vertex_count"],
                    self.VPC["count"],
                    self.VPC["discarded_count"],
                    self.VPC["method"],
                    self.VPC["generation_parameter"],
                    self.optimization["type"],
                    len(self.optimization["coverage_per_vp"]),
                    len(self.optimization["triangle_per_vp"]),
                    len(self.optimization["vp_selection_order"]),
                    len(self.optimization["OVP"]))

# Private
    def __parse_filename(self, log_filename):
        with open(log_filename) as log_file:
            log_data = json.load(log_file)

        try:
            self.__check_file_structure(log_data)
        except Exception as e:
            print("Error: {}".format(e))
            raise Exception("File {} invalid OVP file".format(log_filename))

        self.camera_parameters["focusing_distance_mm"] = log_data["Log"]["Camera"]["DistanceMM"]
        self.camera_parameters["focal_length"] = log_data["Log"]["Camera"]["FocalLength"]
        self.camera_parameters["model"] = log_data["Log"]["Camera"]["Model"]
        self.camera_parameters["pixel_size_mm"] = log_data["Log"]["Camera"]["PixSizeMM"]
        self.camera_parameters["height"] = log_data["Log"]["Camera"]["ResHeight"]
        self.camera_parameters["width"] = log_data["Log"]["Camera"]["ResWidth"]

        self.coverage["triangle_count"] = log_data["Log"]["Coverage"]["InTriangles"]
        self.coverage["percent_fraction"] = log_data["Log"]["Coverage"]["Percentage"]

        self.timing["visibility_matrix_sec"] = log_data["Log"]["Duration"]["RayTracingSec"]
        self.timing["optimization_sec"] = log_data["Log"]["Duration"]["OptimizationSec"]

        self.model["name"] = log_data["Log"]["Model"]["Name"]
        self.model["face_count"] = log_data["Log"]["Model"]["FaceCount"]
        self.model["vertex_count"] = log_data["Log"]["Model"]["VertexCount"]

        self.VPC["count"] = log_data["Log"]["VPC"]["Count"]
        self.VPC["discarded_count"] = log_data["Log"]["VPC"]["DiscardedCount"]
        self.VPC["method"] = log_data["Log"]["VPC"]["Functional"]
        self.VPC["generation_parameter"] = log_data["Log"]["VPC"]["Threshold"]

        self.optimization["type"] = log_data["Log"]["OptimizationType"]
        self.optimization["coverage_per_vp"] = log_data["Log"]["CoveragePerVP"]
        self.optimization["triangle_per_vp"] = log_data["Log"]["TriangleCoveragePerVP"]
        self.optimization["vp_selection_order"] = log_data["Log"]["VPSelectionOrder"]
        self.optimization["OVP"] = log_data["OVP"]["List"]

        self.__check_data()

    # Only checks if the coverage per vp data are of equal length.
    def __check_data(self):
        if ((len(self.optimization["coverage_per_vp"]) != len(self.optimization["triangle_per_vp"])) or \
            (len(self.optimization["triangle_per_vp"]) != len(self.optimization["vp_selection_order"]))):
            raise Exception("'coverage per viewpoint', 'triangle per viewpoint' and " + 
                "'viewpoint selection order' are not of same length!")

    def __check_file_structure(self, log_data):
        if "Log" in log_data:
            if "Camera" in log_data["Log"]:
                if "DistanceMM" not in log_data["Log"]["Camera"]:
                    raise Exception("'Camera' has no 'DistanceMM' entry available.")
                if "FocalLength" not in log_data["Log"]["Camera"]:
                    raise Exception("'Camera' has no 'FocalLength' entry available.")
                if "Model" not in log_data["Log"]["Camera"]:
                    raise Exception("'Camera' has no 'Model' entry available.")
                if "PixSizeMM" not in log_data["Log"]["Camera"]:
                    raise Exception("'Camera' has no 'PixSizeMM' entry available.")
                if "ResHeight" not in log_data["Log"]["Camera"]:
                    raise Exception("'Camera' has no 'ResHeight' entry available.")
                if "ResWidth" not in log_data["Log"]["Camera"]:
                    raise Exception("'Camera' has no 'ResWidth' entry available.")
            else:
                raise Exception("'Log' has no 'Camera' entry available.")

            if "Coverage" in log_data["Log"]:
                if "InTriangles" not in log_data["Log"]["Coverage"]:
                    raise Exception("'Coverage' has no 'InTriangles' entry available.")
                if "Percentage" not in log_data["Log"]["Coverage"]:
                    raise Exception("'Coverage' has no 'Percentage' entry available.")
            else:
                raise Exception("'Log' has no 'Coverage' entry available.")

            if "Duration" in log_data["Log"]:
                if "OptimizationSec" not in log_data["Log"]["Duration"]:
                    raise Exception("'Duration' has no 'OptimizationSec' entry available.")
                if "RayTracingSec" not in log_data["Log"]["Duration"]:
                    raise Exception("'Duration' has no 'RayTracingSec' entry available.")
            else:
                raise Exception("'Log' has no 'Duration' entry available.")

            if "Model" in log_data["Log"]:
                if "FaceCount" not in log_data["Log"]["Model"]:
                    raise Exception("'Model' has no 'FaceCount' entry available.")
                if "Name" not in log_data["Log"]["Model"]:
                    raise Exception("'Model' has no 'Name' entry available.")
                if "VertexCount" not in log_data["Log"]["Model"]:
                    raise Exception("'Model' has no 'VertexCount' entry available.")
            else:
                raise Exception("'Log' has no 'Model' entry available.")

            if "VPC" in log_data["Log"]:
                if "Count" not in log_data["Log"]["VPC"]:
                    raise Exception("'VPC' has no 'Count' entry available.")
                if "DiscardedCount" not in log_data["Log"]["VPC"]:
                    raise Exception("'VPC' has no 'DiscardedCount' entry available.")
                if "Functional" not in log_data["Log"]["VPC"]:
                    raise Exception("'VPC' has no 'Functional' entry available.")
                if "Threshold" not in log_data["Log"]["VPC"]:
                    raise Exception("'VPC' has no 'Threshold' entry available.")
            else:
                raise Exception("'Log' has no 'VPC' entry available.")

            if "CoveragePerVP" not in log_data["Log"]:
                raise Exception("No 'CoveragePerVP' entry available.")
            if "TriangleCoveragePerVP" not in log_data["Log"]:
                raise Exception("No 'TriangleCoveragePerVP' entry available.")
            if "VPSelectionOrder" not in log_data["Log"]:
                raise Exception("No 'VPSelectionOrder' entry available.")
            if "OptimizationType" not in log_data["Log"]:
                raise Exception("No 'OptimizationType' entry available.")
        else:
            raise Exception("No 'Log' entry available.")

        if "OVP" in log_data:
            if "Count" not in log_data["OVP"]:
                raise Exception("'OVP' has no 'Count' entry available.")
            if "List" not in log_data["OVP"]:
                raise Exception("'OVP' has no 'List' entry available.")
        else:
            raise Exception("No 'OVP' entry available.")

# Public
    # Getters
    def get_cumulative_coverage_per_vp(self):
        return self.convert_cumulative(self.optimization["coverage_per_vp"])

    def get_cumulative_triangle_per_vp(self):
        return self.convert_cumulative(self.optimization["triangle_per_vp"])

# Utilities
    def convert_cumulative(self, value_array):
        cumulative_array = []
        for i in range(len(value_array)):
            value = 0
            for j in range(i):
                value += value_array[j]
            cumulative_array.append(value)

        return cumulative_array
