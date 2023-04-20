import digitalio, pwmio, time, board, math
# from adafruit_motor import servo

boardToPins = {
  "unexpectedmaker_feathers2": {
    "rightServoPin": board.D5,
    "leftServoPin": board.D6,
    "leftMotorPin": board.D14,
    "rightMotorPin": board.D15,
    "capSensPin": board.D12,
    "motorEnablePin": board.D16
  },
  "adafruit_feather_esp32s2": {
    "rightServoPin": board.D5,
    "leftServoPin": board.D6,
    "leftMotorPin": board.D9,
    "rightMotorPin": board.D10,
    "capSensPin": board.D12,
    "motorEnablePin": board.D11
  },
  "raspberry_pi_pico": {
    "rightServoPin": board.GP21,
    "leftServoPin": board.GP20,
    "leftMotorPin": board.GP19,
    "rightMotorPin": board.GP18,
    "capSensPin": board.GP17,
    "motorEnablePin": board.GP16
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

    self.rightMotorPin = pwmio.PWMOut(boardToPins[board.board_id]["rightMotorPin"], duty_cycle=0, frequency=1000)
    self.leftMotorPin = pwmio.PWMOut(boardToPins[board.board_id]["leftMotorPin"], duty_cycle=0, frequency=1000)

    self.motorEnable = digitalio.DigitalInOut(boardToPins[board.board_id]["motorEnablePin"])
    self.motorEnable.direction = digitalio.Direction.OUTPUT

    self.capSens = digitalio.DigitalInOut(boardToPins[board.board_id]["capSensPin"])
    self.capSens.direction = digitalio.Direction.INPUT
    self.capSens.pull = digitalio.Pull.UP

    self.sleepSeconds = 2.4
    self.fakeShotSeconds = 4
    self.shootAllGapSeconds = 1
    self.boltGraceSeconds = 0.7

    self.resetState()

  def setServoDutyCycle(self, left, right):
    print("setting duty cycle")
    self.leftServoPin.duty_cycle = left
    self.rightServoPin.duty_cycle = right

  def setMotorDutyCycle(self, left, right):
    print("setting duty cycle")
    self.leftMotorPin.duty_cycle = left
    self.rightMotorPin.duty_cycle = right

  def setServoDutyPerc(self, left, right):
    self.setServoDutyCycle(percToDutyCycle(left), percToDutyCycle(right))

  def setMotorDutyPerc(self, left, right):
    self.setMotorDutyCycle(percToDutyCycle(left), percToDutyCycle(right))

  def boltBack(self):
    print("moving bolt back")
    # self.rightServo.angle = 170
    # self.leftServo.angle = 10
    self.setServoDutyPerc(3.3, 13)
    time.sleep(self.boltGraceSeconds)
    self.turnOffServos()

  def boltForward(self):
    print("moving bolt forward")
    # self.rightServo.angle = 0
    # self.leftServo.angle = 180
    self.setServoDutyPerc(12.8, 2.8)
    time.sleep(self.boltGraceSeconds)
    self.turnOffServos()

  def motorsUp(self):
    print("spinning motors up")
    self.setMotorDutyPerc(60, 60)
    self.motorEnable.value = True

  def motorsDown(self):
    print("spinning motors down")
    self.setMotorDutyPerc(0, 0)
    self.motorEnable.value = False

  def turnOffServos(self):
    print("turning off servos")
    self.setServoDutyCycle(0, 0)

  def hasCapacity(self):
    """Checks for whether there is at least one shot remaining determined by the capacity sensor"""
    # Sensor is low when it detects something
    return True
    hasCap = not self.capSens.value
    if not hasCap:
      print("capacity empty")
    return hasCap

  def resetState(self):
    print("resetting state")
    self.motorsDown()
    self.boltBack()


  def ShootSingleSequence(self):
    print("shooting one")
    if not self.hasCapacity():
      return
    self.motorsUp()
    self.boltBack()
    time.sleep(self.sleepSeconds)
    self.boltForward()
    time.sleep(1)
    self.resetState()

  def ShootAllSequence(self):
    print("shooting all")
    if not self.hasCapacity():
      return
    self.motorsUp()
    self.boltBack()
    time.sleep(self.sleepSeconds)

    while self.hasCapacity():
      time.sleep(self.shootAllGapSeconds)
      self.boltForward()
      self.boltBack()
    self.resetState()

  def FakeShootSequence(self):
    print("fake shooting sequence")
    self.boltBack()
    self.motorsUp()
    time.sleep(self.fakeShotSeconds)
    self.resetState()
