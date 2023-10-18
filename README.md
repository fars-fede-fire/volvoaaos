
# Volvo AAOS

Home Assistant custom component for Volvo with Android Automotive OS

Alpha release. Expect breaking changes!

Based on: https://www.postman.com/andynash/workspace/volvo-apis/request/6009097-bccdee07-3486-43ea-b805-2099a4539820



### Entities

Entity | Type | Description
-- | -- | --
`sensor.{name}_battery_level` | Sensor | Battery charged in %
`sensor.{name}_electric_range` | Sensor | Estimated electric range
`sensor.{name}_estimated_charging_time` | Sensor | Estimated remaining charging time
`sensor.{name}_charging_connection_status` | Sensor | Charging connection status. Possible values: CONNECTION_STATUS_CONNECTED_AC, CONNECTION_STATUS_CONNECTED_DC, CONNECTION_STATUS_DISCONNECTED, CONNECTION_STATUS_UNSPECIFIED
`sensor.{name}_charging_system_status` | Sensor | Charging system status. Possible values: CHARGING_SYSTEM_CHARGING, CHARGING_SYSTEM_IDLE, CHARGING_SYSTEM_FAULT, CHARGING_SYSTEM_UNSPECIFIED
`lock.{name}_lock` | Lock | Car is locked or unlocked and service to lock and unlock car


### Services
Service| Data| Description
-- | -- | --
`volvoaaos.start_climatization` | None | Start climatization for 30 minutes.

This integration is tested with my Volvo XC40 P6 - 2023
