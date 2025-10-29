# PaddleOCR Simple API Server

A simple Flask API for OCR using PaddleOCR.

## API Endpoints

### OCR

* Example curl request

`curl -X POST -F "file=@image.png" http://localhost:5000/ocr`

* Example response

`{"results":[{"confidence":0.934224009513855,"text":"Bigw182"},{"confidence":0.3906244933605194,"text":"["},{"confidence":0.8766525387763977,"text":"Flamingo0-_-"},{"confidence":0.3486069440841675,"text":"1"},{"confidence":0.8858639001846313,"text":"/Spooky Scary Fish.."},{"confidence":0.9424086809158325,"text":"Clappnz"}]`