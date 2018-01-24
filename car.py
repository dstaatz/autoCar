''' Describes the car and how to control it '''

# General Imports
import RPi.GPIO as io

io.setwarnings(False)


class Car:

      # Define defaut pinouts
      D1_DEFAULT = 17
      D2_DEFAULT = 18
      S1_DEFAULT = 23
      S2_DEFAULT = 24

      def __init__(self, D1=D1_DEFAULT, D2=D2_DEFAULT, S1=S1_DEFAULT, S2=S2_DEFAULT, reverse_d=False, reverse_s=False):

            # Pin number settings
            self.D1 = D1
            self.D2 = D2
            self.S1 = S1
            self.S2 = S2

            # Reverse Setting
            self.reverse_d = reverse_s
            self.reverse_s = reverse_y

            # Use pin names not pin numbers
            io.setmode(io.BCM)

            # Setup pin types
            io.setup(self.D1, io.OUT)
            io.setup(self.D2, io.OUT)
            io.setup(self.S1, io.OUT)
            io.setup(self.S2, io.OUT)

      def update(self, x, y):

            pass

      def forward_left(self):

            io.output(self.D1, 1 ^ self.reverse_d)
            io.output(self.D2, 0 ^ self.reverse_d)
            io.output(self.S1, 0 ^ self.reverse_s)
            io.output(self.S2, 1 ^ self.reverse_s)

      def forward(self):

            io.output(self.D1, 1 ^ self.reverse_d)
            io.output(self.D2, 0 ^ self.reverse_d)
            io.output(self.S1, 0 ^ self.reverse_s)
            io.output(self.S2, 0 ^ self.reverse_s)

      def forward_right(self):

            io.output(self.D1, 1 ^ self.reverse_d)
            io.output(self.D2, 0 ^ self.reverse_d)
            io.output(self.S1, 1 ^ self.reverse_s)
            io.output(self.S2, 0 ^ self.reverse_s)

      def back_left(self):

            io.output(self.D1, 0 ^ self.reverse_d)
            io.output(self.D2, 1 ^ self.reverse_d)
            io.output(self.S1, 0 ^ self.reverse_s)
            io.output(self.S2, 1 ^ self.reverse_s)

      def back(self):

            io.output(self.D1, 0 ^ self.reverse_d)
            io.output(self.D2, 1 ^ self.reverse_d)
            io.output(self.S1, 0 ^ self.reverse_s)
            io.output(self.S2, 0 ^ self.reverse_s)
      def forward_left(self):
            
            io.output(self.D1, 0 ^ self.reverse_d)
            io.output(self.D2, 1 ^ self.reverse_d)
            io.output(self.S1, 1 ^ self.reverse_s)
            io.output(self.S2, 0 ^ self.reverse_s)

      def stop(self):

            io.output(self.D1, 0 ^ self.reverse_d)
            io.output(self.D2, 0 ^ self.reverse_d)
            io.output(self.S1, 0 ^ self.reverse_s)
            io.output(self.S2, 0 ^ self.reverse_s)