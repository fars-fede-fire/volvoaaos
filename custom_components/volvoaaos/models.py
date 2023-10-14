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
    operation_id: str = Field(..., alias="operationId")
    data: RechargeData


### Get VIN ###

class VinList(BaseModel):
    vin: str

class Pagination(BaseModel):
    limit: int
    total: int


class GetVinModel(BaseModel):
    status: int
    operation_id: str = Field(..., alias='operationId')
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

class CarLocked(BaseModel):
    name: str
    value: str
    timestamp: str


class FrontLeftDoorOpen(BaseModel):
    name: str
    value: str
    timestamp: str


class FrontRightDoorOpen(BaseModel):
    name: str
    value: str
    timestamp: str


class RearLeftDoorOpen(BaseModel):
    name: str
    value: str
    timestamp: str


class RearRightDoorOpen(BaseModel):
    name: str
    value: str
    timestamp: str


class HoodOpen(BaseModel):
    name: str
    value: str
    timestamp: str


class TailGateOpen(BaseModel):
    name: str
    value: str
    timestamp: str


class TankLidOpen(BaseModel):
    name: str
    value: str
    timestamp: str


class DoorData(BaseModel):
    car_locked: CarLocked = Field(..., alias='carLocked')
    front_left_door_open: FrontLeftDoorOpen = Field(..., alias='frontLeftDoorOpen')
    front_right_door_open: FrontRightDoorOpen = Field(..., alias='frontRightDoorOpen')
    rear_left_door_open: RearLeftDoorOpen = Field(..., alias='rearLeftDoorOpen')
    rear_right_door_open: RearRightDoorOpen = Field(..., alias='rearRightDoorOpen')
    hood_open: HoodOpen = Field(..., alias='hoodOpen')
    tail_gate_open: TailGateOpen = Field(..., alias='tailGateOpen')
    tank_lid_open: TankLidOpen = Field(..., alias='tankLidOpen')


class GetDoorModel(BaseModel):
    status: int
    operation_id: str = Field(..., alias='operationId')
    data: DoorData


class ConnectedVehicleModel(BaseModel):
    door_data: GetDoorModel


class StartClimateData(BaseModel):
    vin: str
    status_code: int = Field(..., alias='statusCode')
    invoke_status: str = Field(..., alias='invokeStatus')
    message: str


class StartClimateModel(BaseModel):
    status: int
    operation_id: str = Field(..., alias='operationId')
    data: StartClimateData

