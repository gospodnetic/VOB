# ViewpointOptimizationBenchmark
Comparison of optimization viewpoint data written in format
```
{
    "Log": {
        "Camera": {
            "DistanceMM": float,
            "FocalLength": float,
            "Model": string,
            "PixSizeMM": float,
            "ResHeight": uint,
            "ResWidth": uint
        },
        "Coverage": {
            "InTriangles": uint,
            "Percentage": float
        },
        "CoveragePerVP": [float, ..., float],
        "Duration": {
            "OptimizationSec": float,
            "RayTracingSec": float
        },
        "Model": {
            "FaceCount": uint,
            "Name": string,
            "VertexCount": uint
        },
        "OptimizationType": string,
        "TimeStamp": string,
        "TriangleCoveragePerVP": [uint, ..., uint],
        "VPC": {
            "Count": uint,
            "DiscardedCount": uint,
            "Functional": string,
            "ListName": string,
            "Threshold": string
        },
        "VPSelectionOrder": [uint, ..., uint]
    },
    "OVP": {
        "Count": uint,
        "List": [array of viewpoint objects]
    }
}
```
## Outputs
Outputs in `/data` directory:
* coverage convergence graphs
* best performance table in LaTex (`performance_table.tex`)
* best performance table with information about the number of discarded viewpoints in LaTex (`performance_table_discarded.tex`)
* complete performance table containing all the optimal viewpoint sets
* average discarded statistic per approach
* average discarded statistic per method

## Test data available at:
https://owncloud.fraunhofer.de/index.php/s/H8jV9rwGN84knzP

## Example call
`python3 vob.py object_space_exploration_per_approach_methods.json ovp_paths.json 2020-08-15`

## Args
[1] `object_space_exploration_per_approach_methods.json` - list of methods names assigned to corresponding approach
[2] `ovp_paths.json` - an array of paths to the directory containing the ovp files (not recursive)
[3] optional string - optional string which will be prepended to the coverage graphs

### `object_space_exploration_per_approach_methods.json` example:
```
{
    "SpaceSampling": [
        "MixedRepositionedNormal",
        "NoDisplacement"],
    "VertexSampling": [
        "VertexBBoxCenter",
        "VertexGronle"],
    "PatchSampling": [
        "Area",
        "NoSubdivision"]
    ]
}
```

### `ovp_paths.json` example:
```
[
    "path/to/OVP/directory/"
]
```
