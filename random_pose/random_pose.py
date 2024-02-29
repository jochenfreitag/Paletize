"""Contains the skill random_pose."""

from absl import logging

from intrinsic.skills.python import proto_utils
from intrinsic.skills.python import skill_interface
from intrinsic.util.decorators import overrides
from intrinsic.world.proto import object_world_refs_pb2
import numpy as np

from random_pose import random_pose_pb2
from intrinsic.motion_planning.proto import motion_specification_pb2
from intrinsic.motion_planning.proto import motion_planner_service_pb2
from intrinsic.world.proto import geometric_constraints_pb2
from intrinsic.icon.equipment import equipment_utils
from intrinsic.icon.python import icon_api
from intrinsic.icon.python import create_action_utils
from intrinsic.icon.python import actions
from intrinsic.world.python.object_world_resources import Frame, KinematicObject, TransformNode
from intrinsic.world.python.object_world_ids import WorldObjectName, FrameName
from intrinsic.math.python import data_types, proto_conversion


class RandomPose(skill_interface.Skill):
    """Implementation of the random_pose skill."""

    def __init__(self) -> None:
        pass

    @overrides(skill_interface.Skill)
    def execute(
        self,
        request: skill_interface.ExecuteRequest[random_pose_pb2.RandomPoseParams],
        context: skill_interface.ExecuteContext
    ) -> None:
        
        # Top level constants
        ROBOT_EQUIPMENT_SLOT: str = "robot"
        ARM_PART_NAME: str = "arm"

        #logging.info(
        #    '"text" parameter passed in skill params: ' + request.params.text
        #)

        # Accessing frames
        # moving_frame: Frame = context.object_world.get_frame(
        #   FrameName("tool_frame"), WorldObjectName("picobot_gripper"))
        # moving_frame: Frame = context.object_world.get_frame("tool_frame", "picobot_gripper")
        moving_frame: Frame = context.object_world.picobot_gripper.tool_frame
        
        # target_frame: Frame = context.object_world.get_frame(
        #   FrameName("target_left"), object_name=)
        # target_frame = context.object_world.get_frame("target_frame", "root")
        target_frame: Frame = context.object_world.target_frame

        # sampl = np.random.uniform(low=0.5, high=13.3, size=(3,))
        # pose_offset: data_types.Pose3 = data_types.Pose3(data_types.Rotation3.from_xyzw((0,1,0,0)))

        pose_goal = geometric_constraints_pb2.PoseEquality(
            moving_frame=moving_frame.transform_node_reference,
            target_frame=target_frame.transform_node_reference,
            # target_frame_offset = proto_conversion.pose_to_proto(pose_offset)
            )

        target = motion_specification_pb2.MotionTarget(
            constraint=geometric_constraints_pb2.GeometricConstraint(
                pose_equality=pose_goal))

        segment = motion_specification_pb2.MotionSegment(target=target)
        motion_specification = motion_specification_pb2.MotionSpecification(motion_segments=[segment])

        # Unpack equipment handles.

        robot_handle = context.resource_handles[ROBOT_EQUIPMENT_SLOT]
        
        # obtaining a kinematics object
        # robot_object = object_world.get_kinematic_object(robot_handle)
        robot_object: KinematicObject = context.object_world.robot

        robot_specification = motion_planner_service_pb2.RobotSpecification(
            robot_reference=motion_planner_service_pb2.RobotReference(
                object_id=object_world_refs_pb2.ObjectReference(
                    by_name=object_world_refs_pb2.ObjectReferenceByName(
                        object_name=robot_object.name
                    )
                )
            ),
            default_cartesian_limits=robot_object.cartesian_limits
        )

        result_trajectory = context.motion_planner.plan_trajectory(
            robot_specification=robot_specification,
            motion_specification=motion_specification
        )

        # equipment_utils.init_icon_client()
        icon_client: icon_api.Client = equipment_utils.init_icon_client(robot_handle)
        icon_client.enable()
        print(icon_client.list_parts())

        with icon_client.start_session([ARM_PART_NAME]) as session:
            tracking_action: actions.Action =\
                create_action_utils.create_trajectory_tracking_action(action_id=1, part = ARM_PART_NAME, trajectory=result_trajectory)
            session.add_actions([tracking_action])
            session.start_action_and_wait(tracking_action)
