from disco.bot import Plugin
import random
import re

# TODO: comment this mess


class RollDicePlugin(Plugin):

  @Plugin.listen('MessageCreate')
  def on_message_create(self, event):
    args = event.content.split();
    if args[0][0]!= '!' or str(event.author) == 'RiceDoller#3067':
      return
    if args[0] == '!r':
      try:
        self.roll_function(event, args[1])
      except Error as e:
        event.reply(e)
        event.reply('Invalid syntax! Usage: !r [optional amount]d[required sides][d optional drop]')

  @Plugin.command('ping')
  def on_ping_command(self, event):
    event.msg.reply('Pong!')
    event.msg.reply(self.test_func())

  @Plugin.command('r', '<dieString:str>')
  def on_roll_command(self, event, dieString):
    self.roll_function(event, dieString)


  def roll_dice(self, numSides, numTimes):
    rolls = []
    for iteration in range(numTimes):
      roll = random.randint(1, numSides)
      rolls.append(roll)
    return rolls
  
  def roll_function(self, event, dieString):
    
    # sum of valid rolls
    result = 0; 

    # string containing result text for each roll
    resultText = ''

    # split arguments into each term
    terms = re.findall(r'[-+]?[^-+]+', dieString)
      
    # array containing non-die terms
    constants = []
   
    resultText = str(event.author).split('#')[0] + " rolls " + dieString + '\n'

    # iterate thru list of terms
    for term in terms:

      # default text when no rolls need to be dropped 
      dropText = ''

      # 0 as the default number of rolls to drop
      numDroppedRolls = 0

      # save a copy of the term to use
      termString = term

      # if 2+ terms, each term after first will be added or subtracted
      if term[0] == '+' or term[0] == '-':
        termString = term[1:]

      # split the term into each possible component of a dice roll
      components = termString.split('d') 

      # if there is only component, no rolling is needed. add/subtract directly 
      if len(components) == 1:
        constants.append((-1 if term[0]=='-' else 1) * int(components[0]))
        continue
      if len(components) == 3:
        numDroppedRolls = int(components[2])

      # lists for each roll and dropped roll
      rolls = []
      droppedRolls = []

      # if the first component in the array is empty, assume 1 die roll
      if components[0] == '':
        components[components.index('')] = 1

      # parse the type of die and number of times to roll it
      iterations = int(components[0])
      die = int(components[1])

      # error check to see if somehow a negative sided die is being rolled 
      if die < 1 or numDroppedRolls >= iterations:
        event.reply('Roll a valid number ya dingus')
        return
      else: 
        # roll for the number of iterations, find the sum, combine with result  
        rolls = self.roll_dice(die, iterations)
        result += (-1 if term[0]=='-' else 1) * sum(rolls)

      # if any rolls need be dropped, do so here    
      tempRolls = rolls.copy()
      for x in range(numDroppedRolls):
        drop = min(tempRolls)
        tempRolls.remove(drop)
        droppedRolls.append(drop)
        result -= drop
        dropText = ' dropping {}'.format(droppedRolls)

      resultText += 'Rolling {}d{}.. Result: {},{} \n'.format(iterations, die, rolls, dropText)
    constantsResult = sum(constants)  
    event.reply('{}Total: {}{} = {}'.format(resultText, result, (str(constantsResult) if constantsResult < 0 else '+' + str(constantsResult)), (result + constantsResult)))
