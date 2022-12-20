from resources import *
from inputs import *
import settings
import enemies


class InStates(Enum):
    TEXT = lambda: text.update()
    TEXT2 = lambda: text2.update()
    TEXT3 = lambda: text3.update()
    TEXT4 = lambda: text4.update()
    STAYPUT = lambda: stayPut.update()
    STAYPUT2 = lambda: stayPut2.update()
    RIGHT = lambda: right.update()
    LEFT = lambda: left.update()
    LEFTTXT2 = lambda: leftTxt2.update()
    LRCTXT = lambda: leftTxt3.update()
    ENDSLEEPNIGHT = lambda: endSleepNight.update()
    ENDWALK = lambda: endWalk.update()
    FOREST = lambda: forestTxt1.update()
    FORESTTXT2 = lambda: forestTxt2.update()
    FLOOKSTICK = lambda: fLookStick.update()
    FREKINDLEFAIL = lambda: fRekindleFire.update()
    BATTLE1 = lambda: battle1.update()
    REKINDLEFIRE = lambda: rekindleFire.update()
    CAMP2 = lambda: camp2.update()
    ENDATTACKNIGHT = lambda: endAttackedNight.update()
    CHOICE4 = lambda: choice4.update()
    CONTTRAVEL = lambda: contTravel.update()
    GOWOODS = lambda: goWoods.update()
    DONOTHING = lambda: doNothing.update()
    RUINBATTLE = lambda: ruinBattle.update()
    RUINBATTLETEXT = lambda: ruinBattleText.update()
    FORESTBATTLETEXT = lambda: forestBattleTest.update()
    FORESTBATTLE = lambda: forestBattle.update()


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


def checkPlayerLeft():
    if settings.player.rect.x < 10:
        settings.player.rect.x = settings.dimensions[0] / 2
        return True
    return False


def checkPlayerRight():
    if settings.player.rect.x > settings.dimensions[0] - 49:
        settings.player.rect.x = settings.dimensions[0] / 2
        return True
    return False


def keyPressed(key):
    print(key, inputs[key])
    if inputs[key]:
        return True
    return False


def timeState(state, newTime):
    global time
    toNextState(state)
    settings.time = newTime


def toGameState(state):
    animations.slideAnimation(state)


def toForest():
    animations.slideAnimation(States.FOREST)
    toNextState(InStates.FOREST)


def checkTime(newTime):
    if settings.time == newTime:
        return True
    return False


def setPlayerDamageAdder(damage, nextState):
    settings.player.damageAdder = damage
    toNextState(nextState)


battle1 = Battle(enemies.Wolf())
ruinBattle = Battle(enemies.RuinBoss())
forestBattle = Battle(enemies.ForestBoss())

text = GameFrame(
    ["Controls:", "Press enter to continue text boxes...", "Other keys will be told when they are needed."],
    [lambda: keyPressed("enter"), lambda: toNextState(InStates.TEXT2)])
text2 = GameFrame(["... You wake up in a mysterious land ...", "... You have memories of you driving a truck ...",
                   "... Now you sit on this dirt road, with no truck in sight ..."],
                  [lambda: keyPressed("enter"), lambda: toNextState(InStates.TEXT3)])
text3 = GameFrame(
    ["... There is a thick forest on either side of the road ...", "... You realize you have a choice ...",
     "... You can either go left, right, or stay put ..."],
    [lambda: keyPressed("enter"), lambda: toNextState(InStates.TEXT4)])
text4 = GameFrame(
    ["... To go left, use A to move ...", "... To go right, use D to move ...", "... To stay put, press S ..."],
    [lambda: checkTime(settings.Time.NIGHT), lambda: toNextState(InStates.STAYPUT2)],
    [lambda: keyPressed("enter"), lambda: text4.disableText()],
    [lambda: keyPressed("s"), lambda: timeState(InStates.STAYPUT, settings.Time.SUNSET)],
    [lambda: checkPlayerRight(), lambda: timeState(InStates.RIGHT, settings.Time.SUNSET)],
    [lambda: checkPlayerLeft(), lambda: timeState(InStates.LEFT, settings.Time.SUNSET)])
stayPut = GameFrame(["... You decide to stay put ...", f"... It is now {settings.times[settings.time]} ...",
                     "... You can either go left, right, or stay put ..."],
                    [lambda: checkTime(settings.Time.NIGHT), lambda: toNextState(InStates.STAYPUT2)],
                    [lambda: keyPressed("enter"), lambda: toNextState(InStates.TEXT4)])
stayPut2 = GameFrame(["... You decide to stay put ...", f"... It is now {settings.times[settings.time]} ...",
                      "... You pass out from exhaustion ..."],
                     [lambda: keyPressed("enter"), lambda: toNextState(InStates.ENDSLEEPNIGHT)])
left = GameFrame(["... You decided to go left. ...",
                  f"... You travel ten miles over the course of 5 hours. It is now {settings.times[settings.time]}. ...",
                  "... Where you stop seems to be exactly where you started. ..."],
                 [lambda: keyPressed("enter"), lambda: toNextState(InStates.LEFTTXT2)])
leftTxt2 = GameFrame(
    ["... You can either sleep on the road, ...", "... go into the forest, ...", "... or keep walking. ..."],
    [lambda: keyPressed("enter"), lambda: toNextState(InStates.LRCTXT)])
leftTxt3 = GameFrame(["... To sleep on the road, press S ...", "... To go into the forest, press W ...",
                      "... To keep walking, use A and D"],
                     [lambda: keyPressed("enter"), lambda: leftTxt3.disableText()],
                     [lambda: keyPressed("s"), lambda: toNextState(InStates.ENDSLEEPNIGHT)],
                     [lambda: keyPressed("w"), lambda: toForest()],
                     [lambda: checkPlayerLeft(), lambda: timeState(InStates.ENDWALK, settings.Time.NIGHT)],
                     [lambda: checkPlayerRight(), lambda: timeState(InStates.ENDWALK, settings.Time.NIGHT)])
right = GameFrame(["... You decided to go right. ...",
                   f"... You travel ten miles over the course of 5 hours. It is now {settings.times[settings.time]}. ...",
                   "... Where you stop seems to be exactly where you started. ..."],
                  [lambda: keyPressed("enter"), lambda: toNextState(InStates.LEFTTXT2)])
endWalk = GameFrame(
    ["... You decide to keep walking ...", "... You eventually pass out from exhaustion ...", "... GAME OVER ..."],
    [lambda: keyPressed("enter"), lambda: toGameState(States.ENDGAMELOSE)])
endSleepNight = GameFrame([f"... While you are sleeping, you are eaten by wolves ...", "", "... YOU LOST ..."],
                          [lambda: keyPressed("enter"), lambda: toGameState(States.ENDGAMELOSE)])
forestTxt1 = GameFrame(
    ["... You entered the forest ...", "... You walk around for a while until you find an abandoned camp ...",
     "... You can either sleep in the tent, rekindle the fire, or look for sticks ..."],
    [lambda: keyPressed("enter"), lambda: toNextState(InStates.FORESTTXT2)])
forestTxt2 = GameFrame(["... To look for sticks, press W ...", "... To rekindle the fire, press S ...",
                        "... To sleep in the tent, press E ..."],
                       [lambda: keyPressed("enter"), lambda: forestTxt2.disableText()],
                       [lambda: keyPressed("w"), lambda: toNextState(InStates.FLOOKSTICK)],
                       [lambda: keyPressed("s"), lambda: toNextState(InStates.FREKINDLEFAIL)],
                       [lambda: keyPressed("e"), lambda: toNextState(InStates.ENDSLEEPNIGHT)])
fLookStick = GameFrame(
    ["... You go out and start looking for some sticks ...", "... You find 6 sticks, one of which is super sharp ...",
     "... Will you take the sticks? Press W to take the sticks, S to go back to the tent ..."],
    [lambda: keyPressed("w"), lambda: setPlayerDamageAdder(5, InStates.BATTLE1)],
    [lambda: keyPressed("s"), lambda: toNextState(InStates.BATTLE1)])
returnToFire = GameFrame([" ... ...", "... You return to the campfire ...", "... ..."],
                         [lambda: keyPressed("enter"), lambda: timeState(InStates.CAMP2, settings.Time.NIGHT)])
camp2 = GameFrame(["... You can either sleep in the tent (S) ...", "... Rekindle the fire (F) ...",
                   "... Or look for more sticks (W) ..."],
                  [lambda: keyPressed("s"), lambda: toNextState(InStates.ENDSLEEPNIGHT)],
                  [lambda: keyPressed("f"), lambda: toNextState(InStates.REKINDLEFIRE)],
                  [lambda: keyPressed("w"), lambda: toNextState(InStates.ENDATTACKNIGHT)])
endAttackedNight = GameFrame(["... You go out in the night ...", "... but are attacked by a wild animal ...",
                              "... Unfortunately, you are killed. GAME OVER. ..."],
                             [lambda: keyPressed("enter"), lambda: toGameState(States.ENDGAMELOSE)])
fRekindleFire = GameFrame(["... You attempt to rekindle the fire ...", "... ...", "... but you fail ..."],
                          [lambda: keyPressed("enter"), lambda: toNextState(InStates.FORESTTXT2)])
rekindleFire = GameFrame(["... You attempt to rekindle the fire ...", "... ...", "... and you succeed! ..."],
                         [lambda: keyPressed("enter"), lambda: setPlayerDamageAdder(12, InStates.CHOICE4)])
choice4 = GameFrame(["... You can either continue travelling (W) ...", "... Go deeper into the woods (F) ...",
                     "... or sit there and do nothing (S) ..."],
                    [lambda: keyPressed("enter"), lambda: choice4.disableText()],
                    [lambda: keyPressed("w"), [lambda: toNextState(InStates.CONTTRAVEL)],
                     [lambda: keyPressed("f"), lambda: toNextState(InStates.GOWOODS)],
                     [lambda: keyPressed("s"), lambda: toNextState(InStates.DONOTHING)]])
contTravel = GameFrame(
    ["... You continued to travel ...", "... You get attacked by bandits ...", "... and are killed. GAME OVER. ..."],
    [lambda: keyPressed("enter"), lambda: toGameState(States.ENDGAMELOSE)])
doNothing = GameFrame(
    ["... You sat at the camp for a while ...", "... you are attacked by a large bear, and are killed ...",
     "... GAME OVER ..."], [lambda: keyPressed("enter"), lambda: toGameState(States.ENDGAMELOSE)])
goWoods = GameFrame(
    ["... You decide to go deeper into the woods ...", "... You come across a large set of ruins in the woods ...",
     "... Do you enter them? (W/F) ..."], [lambda: keyPressed("enter"), lambda: goWoods.disableText()],
    [lambda: keyPressed("w"), lambda: toNextState(InStates.RUINBATTLETEXT)],
    [lambda: keyPressed("f"), lambda: toNextState(InStates.FORESTBATTLETEXT)])
ruinBattleText = GameFrame(["... You enter the ruins but hear a loud growling sound from another part of the ruins ...",
                            "... you being looking around when suddenly ...",
                            "... a large beast jumps out at you! ..."],
                           [lambda: keyPressed("enter"), lambda: toNextState(InStates.RUINBATTLE)])
forestBattleText = GameFrame(
    ["... You step away from the ruins ...", "... There is the sound of a large branch breaking off a tree ...",
     "... You turn around and see a large beast standing over you! ..."],
    [lambda: keyPressed("enter"), lambda: toNextState(InStates.FORESTBATTLE)])
