from buildVersion import version
import speech
from core import postNvdaStartup
from globalPluginHandler import runningPlugins


oldCancelSpeech = speech.cancelSpeech

instance = None

def init():
	global instance
	if not instance:
		instance = WorldVoicePatch()
	


class WorldVoicePatch:
	def __init__(self):
		postNvdaStartup.register(self.patch)
	
	def patch(self):
		wv = self.__findWVInstance()
		if not wv:
			return
		
		wv.hookInstance.end()
		
		if version >= '2024.2':
			speech.speech.pre_speechCanceled.register(self.preSpeechCanceled)
		else:
			speech.cancelSpeech = self.cancelSpeech
		
	
	def preSpeechCanceled(self):
		try:
			from synthDriverHandler import getSynth
			getSynth()._voiceManager.taskManager.reset()
		except:
			pass
		
	
	def cancelSpeech(self):
		self.preSpeechCanceled()
		oldCancelSpeech()
	
	def __findWVInstance(self):
		for plugin in runningPlugins:
			if 'WorldVoice' in str(plugin):
				return plugin
			
		
	
