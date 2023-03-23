import digitalio, pwmio, time
from adafruit_motor import servo

class MotorController:
  def __init__(self, revServoPin, fwdServoPin, motorPin, capSensPin) -> None:
    self.revServoPin = pwmio.PWMOut(revServoPin, duty_cycle=2 ** 15, frequency=50)
    self.revServo = servo.Servo(revServoPin)

    self.fwdServoPin = pwmio.PWMOut(fwdServoPin, duty_cycle=2 ** 15, frequency=50)
    self.fwdServo = servo.Servo(fwdServoPin)
    self.revServo.angle = 180
    self.fwdServo.angle = 10

    self.motor = digitalio.DigitalInOut(motorPin)
    self.motor.direction = digitalio.Direction.OUTPUT

    self.capSens = digitalio.DigitalInOut(motorPin)
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
