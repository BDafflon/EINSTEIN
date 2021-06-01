import RPi.GPIO as GPIO

from time import sleep

from serverRPI.helper import Ordre


class Rover:
    def __init__(self, gpioMode=GPIO.BCM,moteur1A=16,moteur1B=20,moteur1E=21):
        GPIO.setwarnings(False)
        GPIO.setmode(gpioMode)  ##je prefere la numerotation BOARD plutot que BCM
        self.moteur1A = moteur1A  ## premiere entr?e du premier moteur, pin 16
        self.moteur1B = moteur1B  ## deuxieme entr?e du premier moteur, pin 18
        self.moteur1E = moteur1E  ## enable du premier moteur, pin 22
        GPIO.setup(self.Moteur1A, GPIO.OUT)  ## ces trois broches du Raspberry Pi sont des sorties
        GPIO.setup(self.Moteur1B, GPIO.OUT)
        GPIO.setup(self.Moteur1E, GPIO.OUT)
        self.pwm = GPIO.PWM(self.Moteur1E, 100)  ## pwm de la broche 22 a une frequence de 50 H
        self.pwm.start(0)

    def avancer(self, ordre = Ordre.OFF, frequence=0):  # sens c'est soit AV soit AR, frequence de 0 � 100

        if ordre == Ordre.AV:
            print("en avant")

            self.pwm.ChangeDutyCycle(frequence)
            GPIO.output(self.Moteur1A, GPIO.HIGH)
            GPIO.output(self.Moteur1B, GPIO.LOW)

    def reculer(self, ordre = Ordre.OFF, frequence=0):

        if ordre == Ordre.AR:
            print("en arriere")
            self.pwm.ChangeDutyCycle(frequence)
            GPIO.output(self.Moteur1A, GPIO.LOW)
            GPIO.output(self.Moteur1B, GPIO.HIGH)

    def arreter(self,ordre = Ordre.OFF, frequence=0):
        if Ordre == Ordre.OFF:

            print("arret")
            GPIO.output(self.Moteur1A, GPIO.LOW)
            GPIO.output(self.Moteur1B, GPIO.LOW)