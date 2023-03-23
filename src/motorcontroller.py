import digitalio, pwmio, time, board
from adafruit_motor import servo

boardToPins = {
  "unexpectedmaker_feathers2": {
    "revServoPin": board.D5,
    "fwdServoPin": board.D6,
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
    print("detected board {}".format(board.board_id))
    self.revServoPin = pwmio.PWMOut(boardToPins[board.board_id]["revServoPin"], duty_cycle=2**15, frequency=50)
    self.revServo = servo.Servo(self.revServoPin)

    self.fwdServoPin = pwmio.PWMOut(boardToPins[board.board_id]["fwdServoPin"], duty_cycle=2**15, frequency=50)
    self.fwdServo = servo.Servo(self.fwdServoPin)
    self.revServo.angle = 170
    self.fwdServo.angle = 10

    self.motor = digitalio.DigitalInOut(boardToPins[board.board_id]["motorPin"])
    self.motor.direction = digitalio.Direction.OUTPUT

    self.capSens = digitalio.DigitalInOut(boardToPins[board.board_id]["capSensPin"])
    self.capSens.direction = digitalio.Direction.INPUT
    self.capSens.pull = digitalio.Pull.UP
    self.resetState()

  def setAngle(self, fwd, rev):
    self.revServo.angle = rev
    self.fwdServo.angle = fwd

  def boltBack(self):
    print("moving bolt back")
    self.revServo.angle = 170
    self.fwdServo.angle = 10
    time.sleep(0.6)
    self.turnOffServos()

  def boltForward(self):
    print("moving bolt forward")
    self.revServo.angle = 0
    self.fwdServo.angle = 180
    time.sleep(0.6)
    self.turnOffServos()

  def motorUp(self):
    print("spinning motor up")

  def motorDown(self):
    print("spinning motor up")

  def turnOffServos(self):
    print("turning off servos")
    self.revServoPin.duty_cycle = 0
    self.fwdServoPin.duty_cycle = 0

  def hasCapacity(self):
    """Checks for whether there is at least one shot remaining determined by the capacity sensor"""
    # Sensor is low when it detects something
    hasCap = not self.capSense.value
    if not hasCap:
      print("capacity empty")
    return hasCap

  def resetState(self):
    print("resetting state")
    self.motor.value = False
    self.boltBack()


  def ShootSingleSequence(self):
    print("shooting one")
    if not self.hasCapacity():
      return
    self.motor.value = True
    self.boltBack()
    time.sleep(2.4)
    self.boltForward()
    time.sleep(1)
    self.resetState()

  def ShootAllSequence(self):
    print("shooting all")
    if not self.hasCapacity():
      return
    self.motor.value = True
    self.boltBack()
    time.sleep(2)

    while self.hasCapacity():
      time.sleep(1)
      self.boltForward()
      self.boltBack()
    self.resetState()

  def FakeShootSequence(self):
    print("fake shooting sequence")
    self.boltBack()
    self.motor.value = True
    time.sleep(3)
    self.resetState()
