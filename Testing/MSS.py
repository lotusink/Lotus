from mss import mss
from Module import ConnectOpenAI


# Save a screenshot of the 1st monitor
with mss() as act:
    act.shot()