from disco.bot import Plugin
import random


class RollDicePlugin(Plugin):
  @Plugin.command('test')
  def on_roll_command(self, event):
    boop = [6, 5, 4]
    event.msg.reply('testarray')
    event.msg.reply(boop)

  @Plugin.command('ping')
  def on_ping_command(self, event):
    boop = [6, 5, 4]
    event.msg.reply('Pong!')
    event.msg.reply('{}'.format(boop))

  @Plugin.command('r', '<dieString:str>')
  def on_roll_command(self, event, dieString):
    result = 0;
    event.msg.reply('{}'.format(dieString))
    components = dieString.split(r"(?=\-|\+)")
    event.msg.reply('{}'.format(components))
    for component in components:
      componentString = component
      if component[0] == '+' or component[0] == '-':
        componentString = component[1:]
      numbers = componentString.split('d') 
      if len(numbers) == 1:
        result += (-1 if component[0]=='-' else 1) * int(numbers[0])
        continue
      rolls = []
      sumRolls = 0;
      if numbers[0] == '':
        numbers[numbers.index('')] = 1
      iterations = int(numbers[0])
      die = int(numbers[1])
      if die < 1:
        event.msg.reply('Roll a valid number ya dingus')
        return
      else:
        for x in range(iterations):
          roll = random.randint(1, die)
          rolls.append(roll)
          sumRolls = sum(rolls)
          result += (-1 if component[0]=='-' else 1) * roll
    event.msg.reply('Rolling {}.. You rolled {}, totaling {}'.format(dieString, rolls, result))
