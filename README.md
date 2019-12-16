# ZotPonicsRaspPi Quick Start
This is the code for the raspberry pi systems designs of the Smart Hydroponics System, ZotPonics.

## Authors
Sidney Lau: B.S. Computer Science and Engineering Major, Class of 2020, University of California, Irvine

Owen Yang: B.S. Computer Science and Engineering Major, Class of 2020, University of California, Irvine
*********************
# Running ZotPonics Raspberry Pi Code
This section is to help you run the ZotPonics Raspberry Pi Code.
```
python3 ZotPonics_raspipy
```
*********************
# Testing
For you can use the `userSimulate.py` file.

There are two main functions you can use `randomUserInputFactor` and `UserActivateControl` to test pushing daata to the datbase.

*********************
# Documentation on Important Functions
## ZotPonics.run
#### ZotPonics.run(*self,simulateAll=False,temperSim=False,humidSim=False,baseLevelSim=False,ecSim=False*)
This function helps run the main control block logic for your ZotPonics hydroponics system.

> ### Parameters
>
> **simulateAll[bool]**:
>
> **temperSim[bool]**:
>
> **humidSim[bool]**:
>
> **baseLevelSim[bool]**:

## randomUserInputFactor
#### randomUserInputFactors(n=10,sleepTime=5)
This function is located in the `userSimulate.py` file. You can run the function by calling the function in the `if __name__ == "__main__"`

## UserActivateControl
#### UserActivateControl(fans=0,vents=1,lights=0,water=1,notify=1)
This function is located in the `userSimulate.py` file. You can run the function by calling the function in the `if __name__ == "__main__"` block. This function allows you to simulate activate the actuators. The actuators includes the fans, the vent flaps, the lights, the water pump, and a notification system.

> ### Parameters
>
> **fans[int]**: default is 0 for convenience. Toggle between 0 or 1. 1 activates the fans, 0 keeps it off.
>
> **vents[int]**: default is 1 for convenience. Toggle between 0 or 1. 1 opens the vents, 0 keeps it off.
>
> **lights[int]**: default is 0 for convenience. Toggle between 0 or 1. 1 turns on the lights, 0 keeps it off.
>
> **water[int]**: default is 1 for convenience. Toggle between 0 or 1. 1 turns on the water pump, 0 keeps it off.
>
> **notify[int]**: default is 1 for convinience. Toggle between 0 or 1. 1 notifies the users, 0 doesn't send any notifications

> ### Returns
> *None*
