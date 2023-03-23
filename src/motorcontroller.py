import board

class MotorController:
  def __init__(self, revServoPin, fwdServoPin, motorPin, capSensPin) -> None:
    self.revServoPin = revServoPin
    self.fwdServoPin = fwdServoPin
    self.motorPin = motorPin
    self.capSensPin = capSensPin
    # Feather32 S2
    # reverseServo = board.D6
    # forwardServo = board.D5
    # motor = board.D9

  def boltBack():
    print("moving bolt back")

  def boltForward():
    print("moving bolt forward")

  def motorUp():
    print("spinning motor up")

  def motorDown():
    print("spinning motor up")

  def checkCapacity():
    """Checks for whether there is at least one shot remaining determined by the capacity sensor"""
    return True
