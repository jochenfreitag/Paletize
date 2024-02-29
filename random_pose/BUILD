load("@ai_intrinsic_sdks//bazel:skills.bzl", "py_skill", "skill_manifest")
load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")
load("@rules_proto//proto:defs.bzl", "proto_library")

proto_library(
    name = "random_pose_proto",
    srcs = ["random_pose.proto"],
)

py_proto_library(
    name = "random_pose_py_pb2",
    deps = [":random_pose_proto"],
)

skill_manifest(
    name = "random_pose_py_manifest",
    src = "random_pose.manifest.textproto",
    deps = [":random_pose_proto"],
)

py_library(
    name = "random_pose",
    srcs = ["random_pose.py"],
    srcs_version = "PY3",
    deps = [
        ":random_pose_py_pb2",
        "@ai_intrinsic_sdks//intrinsic/skills/proto:equipment_py_pb2",
        "@ai_intrinsic_sdks//intrinsic/skills/python:proto_utils",
        "@ai_intrinsic_sdks//intrinsic/skills/python:skill_interface",
        "@ai_intrinsic_sdks//intrinsic/util:decorators",
        "@com_google_absl_py//absl/logging",
        "@com_google_protobuf//:protobuf_python",
        "@ai_intrinsic_sdks//intrinsic/motion_planning/proto:motion_target_py_pb2",
        "@ai_intrinsic_sdks//intrinsic/icon/python:icon",
        "@ai_intrinsic_sdks//intrinsic/icon/python:create_action_utils",
        "@ai_intrinsic_sdks//intrinsic/icon/proto:types_py_pb2",
        "@ai_intrinsic_sdks//intrinsic/icon/equipment:equipment_utils_py",
        "@ai_intrinsic_sdks//intrinsic/world/proto:object_world_refs_py_pb2",
    ],
)

py_skill(
    name = "random_pose_image",
    manifest = ":random_pose_py_manifest",
    deps = [
      ":random_pose",
      ":random_pose_py_pb2",
    ]
)
