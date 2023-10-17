
# Volvo AAOS

Home Assistant custom component for Volvo with Android Automotive OS

Alpha release. Expect breaking changes!

Based on: https://www.postman.com/andynash/workspace/volvo-apis/request/6009097-bccdee07-3486-43ea-b805-2099a4539820



### Entities

Entity | Type | Description
-- | -- | --
`sensor.{name}_battery_level` | Sensor | Battery charged in %
`lock_{name}_lock` | Lock | Car is locked or unlocked and service to lock and unlock car


### Services
Service| Data| Description
-- | -- | --
`volvoaaos.start_climatization` | None | Start climatization for 30 minutes.
