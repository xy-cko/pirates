from deep_translator import GoogleTranslator
from services.logger import setup_logger

logger = setup_logger(__name__)

class Translator:
    def __init__(self):
        self.en_mn = GoogleTranslator(source='en', target='mn')
        self.en_ja = GoogleTranslator(source='en', target='ja')

    def to_mongolian(self, text):
        try:
            result = self.en_mn.translate(text)
            logger.debug(f"Mongolian translation: {result}")
            return result
        except Exception as e:
            logger.error(f"Mongolian trnaslation eroor: {e}")
            return f"[Mongolian error]"
        
    def to_japanese(self, text):
        try:
            result = self.en_ja.translate(text)
            logger.debug(f"Japanese translation: {result}")
            return result
        except Exception as e:
            logger.error(f"Japanese translation error: {e}")
            return f"[Japanese error]"