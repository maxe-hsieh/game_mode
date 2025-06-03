import addonHandler
import os
import api
import speech
import globalPluginHandler
from . import worldVoicePatch

from config import conf
from logHandler import log
from inputCore import decide_executeGesture
from buildVersion import version
from scriptHandler import script

import ui
from winUser import VK_CONTROL, VK_LCONTROL, VK_RCONTROL

addonHandler.initTranslation()
addonSummary = addonHandler.getCodeAddon().manifest["summary"]


# 舊版 NVDA 使用 monkey patches 的準備
oldSpeak = speech.speech.speak
oldCancelSpeech = speech.cancelSpeech

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.patchChineseFileName()
		worldVoicePatch.init()
		conf.spec['gameMode'] = {
			"switch" : "boolean( default=False)",
		}
		self.switch = bool(conf['gameMode']['switch'])
		self.gesture = None
		self.keyboardIsPressed = False
		decide_executeGesture.register(self.decideCancelSpeech)
		
		if version >= '2024.2':
			speech.speech.pre_speech.register(self.pre_speech)
		else:
			speech.speech.speak = self.speak
		
	
	def patchChineseFileName(self):
		# 將 appModules 當中的亂碼檔名改為中文
		appModulesDir = os.path.join(os.path.dirname(__file__), '..', '..', 'appModules')
		if os.path.exists(os.path.join(appModulesDir, '侠行天下.py')):
			return
		
		try:
			os.rename(os.path.join(appModulesDir, 'aªµñ╤ñU.py'), os.path.join(appModulesDir, '侠行天下.py'))
		except Exception as e:
			log.error('無法將 appModules 中的檔名改為中文：{}'.format(e))
		
	
	def terminate(self):
		conf['gameMode']['switch'] = self.switch
		decide_executeGesture.unregister(self.decideCancelSpeech)
		if version >= '2024.2':
			speech.speech.pre_speech.unregister(self.pre_speech)
		else:
			speech.speech.speak = oldSpeak
		
	
	@script(description=_('Toggle the game mode on or off'), gesture='kb:nvda+shift+g', category=addonSummary)
	def script_toggleSwitch(self, gesture):
		self.switch = not self.switch
		if self.switch:
			ui.message(_('Game mode(On)'))
		else:
			speech.cancelSpeech()
			ui.message(_('Game mode(Off)'))
		
	
	def decideCancelSpeech(self, gesture):
		self.gesture = gesture
		if self.switch and gesture.vkCode not in (VK_CONTROL, VK_LCONTROL, VK_RCONTROL):
			self.keyboardIsPressed = True
			gesture.speechEffectWhenExecuted = None
		
		return True
	
	def pre_speech(self, speechSequence, *args, **kwargs):
		if self.switch and self.keyboardIsPressed:
			oldCancelSpeech()
			self.keyboardIsPressed = False
			
		
	
	# monkey patches
	def speak(self, speechSequence, *args, **kwargs):
		self.pre_speech(speechSequence, *args, **kwargs)
		oldSpeak(speechSequence, *args, **kwargs)
	
