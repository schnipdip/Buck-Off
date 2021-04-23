import time
import os
import busio
import board

# for performance reasons only keep information about the board here.
# call the board state information in the main() loop for accelerator optimization
