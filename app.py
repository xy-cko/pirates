from flask import Flask, request, jsonify
from services.modifier import Modifier
from services.divisor import DivisorCounter
from services.translator import Translator
from services.logger import setup_logger
from services.db_service import log_request_to_db

from db.schema import RequestsLog, init_db

app = Flask(__name__)
logger = setup_logger(__name__)

# Initialize services
modifier = Modifier()
div_counter = DivisorCounter()
translator = Translator()

init_db()

@app.route('/', methods=['POST'])
def translate():
    data = request.get_json(silent=True)
    if not data:
        logger.error("No JSON received")
        log_request_to_db(sentence=None, magic_number=None, error="No JSON received")
        return jsonify({"error": "Invalid request"}), 400
    
    if 'sentence' not in data or 'magic_number' not in data:
        logger.error("Missing sentence or magic number in request")
        log_request_to_db(sentence=data.get('sentence'), magic_number=data.get('magic_number'), error="Missing sentence or magic number")
        return jsonify({"error": "Invalid request"}), 400

    sentence = data.get('sentence')
    magic_number = data.get('magic_number')

    # Validate magic_number
    if magic_number is None or not isinstance(magic_number, (int)):
        logger.info("Magic number missing")
        log_request_to_db(sentence=sentence, magic_number=None, error="Where is magic?")
        return jsonify({"error": "Where is magic?"}), 400

    # Compute pirate count
    pirates_count = div_counter.count_distinct_divisors(magic_number)
    logger.info(f"Pirates count: {pirates_count} from magic {magic_number}")

    # Modify sentence
    modified, error = modifier.modify(sentence, pirates_count)
    if error:
        logger.info(f"Modification error: {error}")
        log_request_to_db(sentence=sentence, magic_number=magic_number, eng_out=None, jap_out=None, mon_out=None, error=error)
        return jsonify({"error": error}), 400

    logger.info(f"Modified English: {modified}")

    # Translate
    mongolian = translator.to_mongolian(modified)
    japanese = translator.to_japanese(modified)
    log_request_to_db(sentence=sentence, magic_number=magic_number, eng_out=modified, jap_out=japanese, mon_out=mongolian, error=None)
    logger.info("Request logged to database.")
    print("Request actually logged to database.")

    response = {
        "english_sentence": modified,
        "mongolian_sentence": mongolian,
        "japanese_sentence": japanese
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)