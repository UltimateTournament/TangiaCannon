import wificontroller, motorcontroller, gc
from time import sleep

wifiController = None
motorController = None

def main():
    print("starting wifi controller")
    wifiController = wificontroller.WiFiController()
    print("starting motor controller")
    motorController = motorcontroller.MotorController()
    print("starting poll loop")
    while True:
        interaction = wifiController.pollInteractions()
        if interaction is None:
            print("got no interaction")
        elif isinstance(interaction, dict):
            print("got interaction json", interaction)
            instruction = interaction["Instruction"]
            executionID = interaction["ExecutionID"]
            if instruction == wifiController.InstructionLaunchOne:
                motorController.ShootSingleSequence()
            elif instruction == wifiController.InstructionLaunchAll:
                motorController.ShootAllSequence()
            elif instruction == wifiController.InstructionLaunchFake:
                motorController.FakeShootSequence()
            else:
                print("Unknown instruction", instruction)
            wifiController.ackInteraction(executionID)
        gc.collect()
        sleep(2)

main()
