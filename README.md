
# Volvo AAOS

Home Assistant custom component for Volvo with Android Automotive OS

Alpha release. Expect breaking changes!



### Entities

Entity | Type | Description
-- | -- | --
`sensor.{name}_battery_level` | Sensor | Battery charged in %
`binary_sensor_{name}_lock_state` | Binary sensor | Car is locked or unlocked


### Services
Service| Data| Description
-- | -- | --
`volvoaaos.start_climatization` | None | Start climatization for 30 minutes.
