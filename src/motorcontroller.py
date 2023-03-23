import digitalio, pwmio, time, board
from adafruit_motor import servo

boardToPins = {
  "unexpectedmaker_feathers2": {
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
  def __init__(self) -> None:
    self.revServoPin = pwmio.PWMOut(boardToPins[board.board_id]["revServoPin"], duty_cycle=2 ** 15, frequency=50)
    self.revServo = servo.Servo(boardToPins[board.board_id]["revServoPin"])

    self.fwdServoPin = pwmio.PWMOut(boardToPins[board.board_id]["fwdServoPin"], duty_cycle=2 ** 15, frequency=50)
    self.fwdServo = servo.Servo(boardToPins[board.board_id]["fwdServoPin"])
    self.revServo.angle = 180
    self.fwdServo.angle = 10

    self.motor = digitalio.DigitalInOut(boardToPins[board.board_id]["motorPin"])
    self.motor.direction = digitalio.Direction.OUTPUT

    self.capSens = digitalio.DigitalInOut(boardToPins[board.board_id]["capSensPin"])
    self.capSens.direction = digitalio.Direction.INPUT
    self.capSens.pull = digitalio.Pull.UP
    self.resetState()

  def boltBack():
    print("moving bolt back")

  def boltForward():
    print("moving bolt forward")

  def motorUp():
    print("spinning motor up")

  def motorDown():
    print("spinning motor up")

  def hasCapacity(self):
    """Checks for whether there is at least one shot remaining determined by the capacity sensor"""
    # Sensor is low when it detects something
    hasCap = not self.capSense.value
    if not hasCap:
      print("capacity empty")
    return hasCap

  def resetState(self):
    print("resetting state")
    self.boltBack()
    self.motor.value = False
    time.sleep(0.6) # time for servos to move


  def ShootSingleSequence(self):
    print("shooting one")
    if not self.hasCapacity():
      return
    self.boltBack()
    self.motor.value = True
    time.sleep(3)
    self.boltForward()
    time.sleep(1)
    self.resetState()

  def ShootAllSequence(self):
    print("shooting all")
    if not self.hasCapacity():
      return
    self.boltBack()
    self.motor.value = True
    time.sleep(2)

    while self.hasCapacity():
      time.sleep(1)
      self.boltForward()
      time.sleep(0.6)
      self.boltBack()
    self.resetState()

  def FakeShootSequence(self):
    print("fake shooting sequence")
    self.prepareToShoot()
    time.sleep(1) # sleep an extra second
    self.resetState()
