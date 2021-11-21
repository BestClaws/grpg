class Event:

    # event constants.
    ACTION_AUTO = 0x001
    ACTION_CHARGE = 0x002
    ACTION_SKILL = 0x003
    ACTION_BURST = 0x004
    ACTION_SWITCH = 0X009
    CHARA_FOCUS = 0x005
    CHARA_BLUR = 0.006
    CHARA_FALL = 0x007
    CHARA_REVIVE = 0x008

    def __init__(self, type, val=None):
        self.type = type
        self.val = val
        


if __name__ == '__main__':
    print(Event.Action.AUTO)