package(default_visibility = [":internal"])

licenses(["notice"])  # Apache 2.0

exports_files(["LICENSE"])

package_group(
    name = "internal",
    packages = [
        "//im2txt/...",
    ],
)

py_binary(
    name = "build_mscoco_data",
    srcs = [
        "data_scripts/build_mscoco_data.py",
    ],
)

py_binary(
    name = "build_meme_data",
    srcs = [
        "data_scripts/build_meme_data.py",
    ],
)

sh_binary(
    name = "download_and_preprocess_mscoco",
    srcs = ["data_scripts/download_and_preprocess_mscoco.sh"],
    data = [
        ":build_mscoco_data",
    ],
)

sh_binary(
    name = "process_meme_json",
    srcs = ["data_scripts/process_meme_json.sh"],
    data = [
	":build_meme_data",
    ],
)

sh_binary(
    name = "download_inception",
    srcs = ["data_scripts/download_inception.sh"],
)

py_library(
    name = "configuration",
    srcs = ["configuration.py"],
    srcs_version = "PY2AND3",
)

py_library(
    name = "show_and_tell_model",
    srcs = ["show_and_tell_model.py"],
    srcs_version = "PY2AND3",
    deps = [
        "//im2txt/ops:image_embedding",
        "//im2txt/ops:image_processing",
        "//im2txt/ops:inputs",
    ],
)

py_test(
    name = "show_and_tell_model_test",
    size = "large",
    srcs = ["show_and_tell_model_test.py"],
    deps = [
        ":configuration",
        ":show_and_tell_model",
    ],
)

py_library(
    name = "inference_wrapper",
    srcs = ["inference_wrapper.py"],
    srcs_version = "PY2AND3",
    deps = [
        ":show_and_tell_model",
        "//im2txt/inference_utils:inference_wrapper_base",
    ],
)

py_binary(
    name = "train",
    srcs = ["train.py"],
    srcs_version = "PY2AND3",
    deps = [
        ":configuration",
        ":show_and_tell_model",
    ],
)

py_binary(
    name = "evaluate",
    srcs = ["evaluate.py"],
    srcs_version = "PY2AND3",
    deps = [
        ":configuration",
        ":show_and_tell_model",
    ],
)

py_binary(
    name = "run_inference",
    srcs = ["run_inference.py"],
    srcs_version = "PY2AND3",
    deps = [
        ":configuration",
        ":inference_wrapper",
        "//im2txt/inference_utils:caption_generator",
        "//im2txt/inference_utils:vocabulary",
    ],
)
