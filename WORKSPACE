workspace(name="random_pose")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "ai_intrinsic_sdks",
    remote = "https://github.com/intrinsic-dev/intrinsic_sdks",
    tag = "v1.4.20240214",
)

# Load shared dependencies for Intrinsic SDKs. None of these is optional.
load("@ai_intrinsic_sdks//bazel:deps_0.bzl", "intrinsic_sdks_deps_0")
intrinsic_sdks_deps_0()
load("@ai_intrinsic_sdks//bazel:deps_1.bzl", "intrinsic_sdks_deps_1")
intrinsic_sdks_deps_1()
load("@ai_intrinsic_sdks//bazel:deps_2.bzl", "intrinsic_sdks_deps_2")
intrinsic_sdks_deps_2()
load("@ai_intrinsic_sdks//bazel:deps_3.bzl", "intrinsic_sdks_deps_3")
intrinsic_sdks_deps_3()
