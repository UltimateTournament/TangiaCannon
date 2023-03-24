import digitalio, pwmio, time, board, math
from adafruit_motor import servo

boardToPins = {
  "unexpectedmaker_feathers2": {
    "rightServoPin": board.D5,
    "leftServoPin": board.D6,
    "motorPin": board.D9,
    "capSensPin": board.D12
  },
  "esp32s2feather": {
    "rightServoPin": board.D6,
    "leftServoPin": board.D5,
    "motorPin": board.D9,
    "capSensPin": board.D10
  }
}

def percToDutyCycle(perc):
  """
  Converts a milliseconds to a duty cycle. 2.5 to 12.5 is real range
  https://raspberrypi.stackexchange.com/questions/106858/what-is-the-proper-calculation-of-duty-cycle-range-for-the-sg90-servo
  """
  return math.trunc((perc/100)*(65535))

class MotorController:
  def __init__(self) -> None:
    print("detected board {}".format(board.board_id))
    self.rightServoPin = pwmio.PWMOut(boardToPins[board.board_id]["rightServoPin"], duty_cycle=2**15, frequency=50)

    self.leftServoPin = pwmio.PWMOut(boardToPins[board.board_id]["leftServoPin"], duty_cycle=2**15, frequency=50)

    self.motor = digitalio.DigitalInOut(boardToPins[board.board_id]["motorPin"])
    self.motor.direction = digitalio.Direction.OUTPUT

    self.capSens = digitalio.DigitalInOut(boardToPins[board.board_id]["capSensPin"])
    self.capSens.direction = digitalio.Direction.INPUT
    self.capSens.pull = digitalio.Pull.UP
    self.resetState()

  def setDutyCycle(self, left, right):
    print("setting duty cycle")
    self.leftServoPin.duty_cycle = left
    self.rightServoPin.duty_cycle = right

  def setDutyPerc(self, left, right):
    self.setDutyCycle(percToDutyCycle(left), percToDutyCycle(right))

  def boltBack(self):
    print("moving bolt back")
    # self.rightServo.angle = 170
    # self.leftServo.angle = 10
    self.setDutyPerc(3.3, 13)
    time.sleep(0.7)
    self.turnOffServos()

  def boltForward(self):
    print("moving bolt forward")
    # self.rightServo.angle = 0
    # self.leftServo.angle = 180
    self.setDutyPerc(12.8, 2.8)
    time.sleep(0.7)
    self.turnOffServos()

  def motorUp(self):
    print("spinning motor up")

  def motorDown(self):
    print("spinning motor up")

  def turnOffServos(self):
    print("turning off servos")
    self.setDutyCycle(0, 0)

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
