import os

MEME_LIB = {}
FONTS = {}

BASEDIR_NAME = os.path.dirname(__file__)
BASEDIR_PATH = os.path.abspath(BASEDIR_NAME)

KOKAINUM_TAGS = ('kokainum', 'кокаинум')
SANDMAN_TAGS = ('mrsandman', 'sandman', 'сэндмен', 'mr sandman')
CATGIRLS_TAGS = ('girlscat','catgirls', 'девкикот', '2девки1кот')
WOLF_TAGS = ('wolf', 'волк')
BOYFRIEND_TAGS = ('boyfriend', 'бойфренд')
BRAIN_TAGS = ('brain', 'мозг', 'мегамозг', 'brain3', 'brain4', 'brain5')
CRYING_TAGS = ('crying', 'плач', 'кот плачет', 'плачущий кот')
TORERO_TAGS = ('torero', 'toreador', 'тореро', 'тореадор')
CHANEL_ID = '-1001423481095'

TAGS_STRING = ''

HELP_STRING = """First string - tag, second and subsequent lines are inscriptions.

Example:
@MemeMkrBot girlscat
Message 1
Message 2

If the tag is not found - you can send a white picture with the inscription.
Example:
@MemeMkrBot unknow_tag
Message 1
"""