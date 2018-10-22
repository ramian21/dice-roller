from disco.bot import Plugin
import random


class TutorialPlugin(Plugin):
  @Plugin.command('ping')
  def on_ping_command(self, event):
    event.msg.reply('Pong!')

  @Plugin.command('echo', '<content:str...>')
  def on_echo_command(self, event, content):
    event.msg.reply(content)

  @Plugin.command('add', '<a:int> <b:int>')
  def on_add_command(self, event, a, b):
    event.msg.reply('{}'.format(a+b))
    event.msg.reply('Rolling d{}.. You rolled a {}'.format(a, b))

  @Plugin.command('roll', '<die:int>')
  def on_roll_command(self, event, die):
    roll = random.randint(1, die)
    event.msg.reply('Rolling d{}.. You rolled a {}'.format(die, roll))

  tags = {}
  @Plugin.command('tag', '<name:str> [value:str...]')
  def on_tag_command(self, event, name, value=None):
    event.msg.reply('test')
    if value:
      tags[name] = value
      event.msg.reply(':ok_hand: created tag `{}`'.format(name))
    else:
      if name in tags.keys():
        return event.msg.reply(tags[name])
      else:
        return event.msg.reply('Unknown tag: `{}`'.format(name))
