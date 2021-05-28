from .Minmaxers.HelpInvoker import HelpInvoker
from .Minmaxers.Highriser import Highriser
from .Minmaxers.Highriser2 import Highriser2
from .Minmaxers.LowIsGood import LowIsGood
from .Minmaxers.RooflessCuddler import RooflessCuddler
from .Minmaxers.SimpleInvoker import SimpleInvoker
from .Santorini import Santorini

INSTANCES = {'RandomMinmaxer' : Santorini(False),
             'LowIsGood' : LowIsGood(False),
             'Highriser2' : Highriser2(False),
             'Highriser' : Highriser(False),
             'HelpInvoker' : HelpInvoker(False),
             'RooflessCuddler' : RooflessCuddler(False),
             'SimpleInvoker' : SimpleInvoker(False)}