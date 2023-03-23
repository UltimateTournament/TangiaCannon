import digitalio, pwmio, time, board
from adafruit_motor import servo

boardToPins = {
  "feathers2": {
    "revServoPin": board.D6,
    "fwdServoPin": board.D5,
    "motorPin": board.D9,
    "capSensPin": board.D12
  },
  "esp32s2feather": {
    "revServoPin": board.D6,
    "fwdServoPin": board.D5,
    "motorPin": board.D9,
    "capSensPin": board.D10
  }
}

class MotorController:
  def __init__(self, boardID) -> None:
    self.revServoPin = pwmio.PWMOut(boardToPins[boardID]["revServoPin"], duty_cycle=2 ** 15, frequency=50)
    self.revServo = servo.Servo(boardToPins[boardID]["revServoPin"])

    self.fwdServoPin = pwmio.PWMOut(boardToPins[boardID]["fwdServoPin"], duty_cycle=2 ** 15, frequency=50)
    self.fwdServo = servo.Servo(boardToPins[boardID]["fwdServoPin"])
    self.revServo.angle = 180
    self.fwdServo.angle = 10

    self.motor = digitalio.DigitalInOut(boardToPins[boardID]["motorPin"])
    self.motor.direction = digitalio.Direction.OUTPUT

    self.capSens = digitalio.DigitalInOut(boardToPins[boardID]["capSensPin"])
    self.capSens.direction = digitalio.Direction.INPUT
    self.capSens.pull = digitalio.Pull.UP
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
    return self.capSense.value
