from dotenv import load_dotenv
import os
from collections import defaultdict, deque
streamers = {}
COMMENTS = defaultdict(lambda: deque(maxlen=500))