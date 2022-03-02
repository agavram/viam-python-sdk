from grpclib.server import Stream
from viam.components.service_base import ComponentServiceBase
from viam.errors import ComponentNotFoundError
from viam.proto.api.component.imu import (
    IMUServiceBase,
    ReadOrientationRequest, ReadOrientationResponse,
    ReadAngularVelocityRequest, ReadAngularVelocityResponse,
    ReadAccelerationRequest, ReadAccelerationResponse,
)

from .imu import IMUBase


class IMUService(IMUServiceBase, ComponentServiceBase[IMUBase]):
    """
    gRPC Service for an IMU
    """

    RESOURCE_TYPE = IMUBase

    async def ReadAngularVelocity(
        self,
        stream: Stream[ReadAngularVelocityRequest, ReadAngularVelocityResponse]
    ) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        try:
            imu = self.get_component(name)
        except ComponentNotFoundError as e:
            raise e.grpc_error()
        velocity = await imu.read_angular_velocity()
        response = ReadAngularVelocityResponse(angular_velocity=velocity)
        await stream.send_message(response)

    async def ReadOrientation(
        self,
        stream: Stream[ReadOrientationRequest, ReadOrientationResponse]
    ) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        try:
            imu = self.get_component(name)
        except ComponentNotFoundError as e:
            raise e.grpc_error()
        orientation = await imu.read_orientation()
        response = ReadOrientationResponse(
            orientation=orientation.euler_angles)
        await stream.send_message(response)

    async def ReadAcceleration(
        self,
        stream: Stream[ReadAccelerationRequest, ReadAccelerationResponse]
    ) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        try:
            imu = self.get_component(name)
        except ComponentNotFoundError as e:
            raise e.grpc_error()
        acceleration = await imu.read_acceleration()
        response = ReadAccelerationResponse(acceleration=acceleration)
        await stream.send_message(response)