from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import logging
import os
import traceback

app = Flask(__name__)

ocr = None


def initialize_ocr():
    global ocr
    try:
        ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )
        app.logger.info("PaddleOCR initialized successfully")
    except Exception as e:
        app.logger.error(f"Failed to initialize PaddleOCR: {str(e)}")
        raise


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})


@app.route('/ocr', methods=['POST'])
def process_ocr():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if ocr is None:
            return jsonify({"error": "OCR engine not initialized"}), 500

        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)

        result = ocr.predict(input=temp_path)

        os.remove(temp_path)

        if not result:
            return jsonify({"results": []})

        results = []
        for page in result:
            for i, text in enumerate(page.get('rec_texts', [])):
                results.append({
                    "text": text,
                    "confidence": float(page.get('rec_scores', [])[i]) if i < len(page.get('rec_scores', [])) else 0.0
                })

        return jsonify({"results": results})

    except Exception as e:
        app.logger.error(f"OCR processing error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    initialize_ocr()
    from waitress import serve
    import multiprocessing

    threads = multiprocessing.cpu_count()
    serve(app, host='0.0.0.0', port=5000, threads=threads)