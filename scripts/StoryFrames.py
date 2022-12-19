from resources import *
from settings import *
from inputs import *
import enemies


class InStates(Enum):
    TEXT = lambda: text.update()
    TEXT2 = lambda: text2.update()
    TEXT3 = lambda: text3.update()
    TEXT4 = lambda: text4.update()
    STAYPUT = lambda: stayPut.update()
    STAYPUT2 = lambda: stayPut2.update()
    RIGHT = lambda: right.update()
    RIGHTTEXT2 = lambda: rightTxt2.update()
    LEFT = lambda: left.update()
    LEFTTXT2 = lambda: leftTxt2.update()
    LRCTXT = lambda: leftTxt3.update()
    ENDSLEEPNIGHT = lambda: endSleepNight.update()
    ENDWALK = lambda: endWalk.update()
    FOREST = lambda: forestTxt1.update()
    FORESTTXT2 = lambda: forestTxt2.update()
    FLOOKSTICK = lambda: fLookStick.update()
    FREKINDLEFAIL = lambda: fRekindleFail.update()
    BATTLE1 = lambda: battle1.update()

timerCount = 0
inState = InStates.TEXT

def timer(ticks):
    global timerCount
    if timerCount > ticks:
        return True
    else:
        timerCount += 1
        return False


def toNextState(newState):
    global inState, timerCount
    inState = newState
    timerCount = 0

def checkPlayerRight():
    if player.rect.x < 1:
        return True
    return False


def checkPlayerLeft():
    if player.rect.x > dimensions[0] - 39:
        return True
    return False


def keyPressed(key):
    if inputs[key]:
        return True
    return False

def timeState(state, newTime):
    global time
    toNextState(state)
    time = newTime

def toGameState(state):
    animations.slideAnimation(state)

def toForest():
    animations.slideAnimation(States.FOREST)
    toNextState(InStates.FOREST)

def checkTime(newTime):
    if time == newTime:
        return True
    return False

battle1 = Battle(settings.player, enemies.Wolf())

text = GameFrame(["Controls:","Press enter to continue text boxes...","Other keys will be told when they are needed."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.TEXT2)])
text2 = GameFrame(["... You wake up in a mysterious land ...","... You have memories of you driving a truck ...","... Now you sit on this dirt road, with no truck in sight ..."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.TEXT3)])
text3 = GameFrame(["... There is a thick forest on either side of the road ...","... You realize you have a choice ...","... You can either go left, right, or stay put ..."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.TEXT4)])
text4 = GameFrame(["... To go left, use A to move ...","... To go right, use D to move ...","... To stay put, press S ..."],[lambda: checkTime(Time.NIGHT), lambda: toNextState(InStates.STAYPUT2)],[lambda: keyPressed("enter"),lambda: text4.disableText()],[lambda: keyPressed("s"),lambda: timeState(InStates.STAYPUT, Time.SUNSET)],[lambda: checkPlayerRight(),lambda: timeState(InStates.RIGHT, Time.SUNSET)],[lambda: checkPlayerLeft(),lambda: timeState(InStates.LEFT, Time.SUNSET)])
stayPut = GameFrame(["... You decide to stay put ...",f"... It is now {times[time]} ...","... You can either go left, right, or stay put ..."],[lambda: checkTime(Time.NIGHT), lambda: toNextState(InStates.STAYPUT2)],[lambda: keyPressed("enter"),lambda: toNextState(InStates.TEXT4)])
stayPut2 = GameFrame(["... You decide to stay put ...",f"... It is now {times[time]} ...","... You pass out from exhaustion ..."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.ENDSLEEPNIGHT)])
left = GameFrame(["... You decided to go left. ...",f"... You travel ten miles over the course of 5 hours. It is now {times[time]}. ...","... Where you stop seems to be exactly where you started. ..."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.LEFTTXT2)])
leftTxt2 = GameFrame(["... You can either sleep on the road, ...","... go into the forest, ...","... or keep walking. ..."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.LRCTXT)])
leftTxt3 = GameFrame(["... To sleep on the road, press S ...","... To go into the forest, press W ...","... To keep walking, use A and D"],[lambda: keyPressed("enter"),lambda: leftTxt3.disableText()],[lambda: keyPressed("s"),lambda: toNextState(InStates.ENDSLEEPNIGHT)],[lambda: keyPressed("w"),lambda: toForest()],[lambda: checkPlayerLeft(),lambda: timeState(InStates.ENDWALK, Time.NIGHT)],[lambda: checkPlayerRight(),lambda: timeState(InStates.ENDWALK, Time.NIGHT)])
right = GameFrame(["... You decided to go right. ...",f"... You travel ten miles over the course of 5 hours. It is now {times[time]}. ...","... Where you stop seems to be exactly where you started. ..."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.RIGHTTEXT2)])
rightTxt2 = GameFrame(["... You can either sleep on the road, ...","... go into the forest, ...","... or keep walking. ..."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.LRCTXT)])
endWalk = GameFrame(["... You decide to keep walking ...","... You eventually pass out from exhaustion ...","... GAME OVER ..."],[lambda: keyPressed("enter"),lambda: toGameState(States.ENDGAMELOSE)])
endSleepNight = GameFrame([f"... While you are sleeping, you are eaten by wolves ...","","... YOU LOST ..."],[lambda: keyPressed("enter"),lambda: toGameState(States.ENDGAMELOSE)])
forestTxt1 = GameFrame(["... You entered the forest ...","... You walk around for a while until you find an abandoned camp ...","... You can either sleep in the tent, rekindle the fire, or look for sticks ..."],[lambda: keyPressed("enter"),lambda: toNextState(InStates.FORESTTXT2)])
forestTxt2 = GameFrame(["... To look for sticks, press W ...","... To rekindle the fire, press S ...","... To sleep in the tent, press E ..."],[lambda: keyPressed("enter"),lambda: forestTxt2.disableText()],[lambda: keyPressed("w"),lambda: toNextState(InStates.FLOOKSTICK)],[lambda: keyPressed("s"),lambda: toNextState(InStates.FREKINDLEFAIL)],[lambda: keyPressed("e"),lambda: toNextState(InStates.ENDSLEEPNIGHT)])
fLookStick = GameFrame(["... You go out and start looking for some sticks ...",
                        "... You find 6 sticks, one of which is super sharp ...",
                        "... Will you take the sticks? Press W to take the sticks, S to go back to the tent ..."],
                       [lambda: keyPressed("w"),
                        lambda: toNextState(InStates.BATTLE1)])


