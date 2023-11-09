"""Models for Volvo AAOS"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

### Authentication ###

class AuthModel(BaseModel):
    """Model for auth"""

    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

### Recharge status ###

class BatteryChargeLevel(BaseModel):
    value: float
    unit: str
    timestamp: str


class ElectricRange(BaseModel):
    value: str
    unit: str
    timestamp: str


class EstimatedChargingTime(BaseModel):
    value: str
    unit: str
    timestamp: str


class ChargingConnectionStatus(BaseModel):
    value: str
    timestamp: str


class ChargingSystemStatus(BaseModel):
    value: str
    timestamp: str




class RechargeData(BaseModel):
    battery_charge_level: BatteryChargeLevel = Field(..., alias="batteryChargeLevel")
    electric_range: ElectricRange = Field(..., alias="electricRange")
    estimated_charging_time: EstimatedChargingTime = Field(
        ..., alias="estimatedChargingTime"
    )
    charging_connection_status: ChargingConnectionStatus = Field(
        ..., alias="chargingConnectionStatus"
    )
    charging_system_status: ChargingSystemStatus = Field(
        ..., alias="chargingSystemStatus"
    )


class RechargeModel(BaseModel):
    status: int
    operation_id: str = Field(..., alias='operationId')
    data: RechargeData


class BatteryChargeLevelData(BaseModel):
    battery_charge_level: BatteryChargeLevel = Field(..., alias='batteryChargeLevel')


class BatteryChargeLevelModel(BaseModel):
    status: int
    operation_id: str = Field(..., alias='operationId')
    data: BatteryChargeLevelData


class BatteryChargeLevelConnectedVehicle(BaseModel):
    value: str
    unit: str
    timestamp: str


class BatteryChargeLevelConnectedVehicleData(BaseModel):
    battery_charge_level: BatteryChargeLevelConnectedVehicle = Field(..., alias='batteryChargeLevel')


class BatteryChargeLevelConnectedVehicleModel(BaseModel):
    status: int
    operation_id: str = Field(..., alias='operationId')
    data: BatteryChargeLevelConnectedVehicleData



### Get VIN ###

class VinList(BaseModel):
    vin: str

class Pagination(BaseModel):
    limit: int
    total: int
    offset: int


class GetVinModel(BaseModel):
    data: List[VinList]
    pagination: Pagination

### Get vehicle data ###

class Images(BaseModel):
    exterior_default_url: str = Field(..., alias='exteriorDefaultUrl')
    interior_default_url: str = Field(..., alias='interiorDefaultUrl')


class Descriptions(BaseModel):
    model: str
    upholstery: str
    steering: str


class GetVehicleData(BaseModel):
    model_year: str = Field(..., alias='modelYear')
    vin: str
    external_colour: str = Field(..., alias='externalColour')
    gearbox: str
    fuel_type: str = Field(..., alias='fuelType')
    images: Images
    descriptions: Descriptions


class GetVehicleModel(BaseModel):
    status: int
    operation_id: str = Field(..., alias='operationId')
    data: GetVehicleData

### Get door status ###

class CentralLock(BaseModel):
    value: str
    timestamp: str


class FrontLeftDoor(BaseModel):
    value: str
    timestamp: str


class FrontRightDoor(BaseModel):
    value: str
    timestamp: str


class RearLeftDoor(BaseModel):
    value: str
    timestamp: str


class RearRightDoor(BaseModel):
    value: str
    timestamp: str


class Hood(BaseModel):
    value: str
    timestamp: str


class Tailgate(BaseModel):
    value: str
    timestamp: str


class TankLid(BaseModel):
    value: str
    timestamp: str


class DoorData(BaseModel):
    central_lock: CentralLock = Field(..., alias='centralLock')
    front_left_door: FrontLeftDoor = Field(..., alias='frontLeftDoor')
    front_right_door: FrontRightDoor = Field(..., alias='frontRightDoor')
    rear_left_door: RearLeftDoor = Field(..., alias='rearLeftDoor')
    rear_right_door: RearRightDoor = Field(..., alias='rearRightDoor')
    hood: Hood
    tailgate: Tailgate
    tank_lid: TankLid = Field(..., alias='tankLid')


class GetDoorModel(BaseModel):
    data: DoorData


class FrontLeftWindow(BaseModel):
    value: str
    timestamp: str


class FrontRightWindow(BaseModel):
    value: str
    timestamp: str


class RearLeftWindow(BaseModel):
    value: str
    timestamp: str


class RearRightWindow(BaseModel):
    value: str
    timestamp: str


class Sunroof(BaseModel):
    value: str
    timestamp: str


class GetWindowData(BaseModel):
    front_left_window: FrontLeftWindow = Field(..., alias='frontLeftWindow')
    front_right_window: FrontRightWindow = Field(..., alias='frontRightWindow')
    rear_left_window: RearLeftWindow = Field(..., alias='rearLeftWindow')
    rear_right_window: RearRightWindow = Field(..., alias='rearRightWindow')
    sunroof: Sunroof


class GetWindowModel(BaseModel):
    data: GetWindowData



class ConnectedVehicleModel(BaseModel):
    door_data: GetDoorModel


class StartClimateData(BaseModel):
    vin: str
    invoke_status: str = Field(..., alias='invokeStatus')
    message: str


class StartClimateModel(BaseModel):
    data: StartClimateData


class StopClimateData(BaseModel):
    vin: str
    invokeStatus: str
    message: str


class StopClimateModel(BaseModel):
    data: StopClimateData


class LockData(BaseModel):
    vin: str
    invokeStatus: str
    message: str


class LockModel(BaseModel):
    data: LockData

class UnlockData(BaseModel):
    vin: str
    invoke_status: str = Field(..., alias='invokeStatus')
    message: str
    ready_to_unlock: bool = Field(..., alias='readyToUnlock')
    ready_to_unlock_until: int = Field(..., alias='readyToUnlockUntil')


class UnlockModel(BaseModel):
    data: UnlockData

class Properties(BaseModel):
    heading: str
    timestamp: str


class Geometry(BaseModel):
    type: str
    coordinates: List[float]


class LocationData(BaseModel):
    type: str
    properties: Properties
    geometry: Geometry


class LocationModel(BaseModel):
    status: int
    operationId: str
    data: LocationData
