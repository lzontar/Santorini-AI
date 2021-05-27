import os
from pathlib import Path

from pathlib import Path
p = Path(__file__)
ALL_MINMAXERS =  [i.split('.')[0] for i in os.listdir(str(p.parent.absolute()) + '/Minmaxers') if i[0] != '_']
