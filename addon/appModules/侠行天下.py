import appModuleHandler
from buildVersion import version
import api
import speech


oldSpeak = speech.speech.speak

class AppModule(appModuleHandler.AppModule):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if version >= '2024.2':
			speech.speech.filter_speechSequence.register(self.filter_speechSequence)
		else:
			speech.speech.speak = self.speak
		
	
	def terminate(self):
		if version >= '2024.2':
			speech.speech.filter_speechSequence.unregister(self.filter_speechSequence)
		else:
			speech.speech.speak = oldSpeak
		
	
	def filter_speechSequence(self, speechSequence):
		if api.getForegroundObject().appModule.appName == '侠行天下':
			while '空白' in speechSequence:
				speechSequence.remove('空白')
			
		
		return speechSequence
	
	def speak(self, speechSequence, *args, **kwargs):
		speechSequence = self.filter_speechSequence(speechSequence)
		oldSpeak(speechSequence, *args, **kwargs)
	
