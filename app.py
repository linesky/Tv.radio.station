from flask import Flask, render_template, send_from_directory, request, Response
import os
#pip install Flask numpy
app = Flask(__name__)

# Diretório onde os arquivos multimédia estão armazenados
FILES_DIR = 'files'

@app.route('/')
def index():
    # Lista todos os arquivos no diretório FILES_DIR
    files = os.listdir(FILES_DIR)
    return render_template('index.html', files=files)

@app.route('/stream/<filename>')
def stream_file(filename):
    return render_template('stream.html', filename=filename)

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(FILES_DIR, filename)

def generate_range_response(path, start, end=None):
    file_size = os.path.getsize(path)
    end = end or file_size - 1
    length = end - start + 1

    with open(path, 'rb') as f:
        f.seek(start)
        data = f.read(length)
    
    headers = {
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(length),
        'Content-Type': 'video/mp4'  # Ajuste conforme o tipo de arquivo
    }
    
    return Response(data, headers=headers, status=206)

@app.route('/files/<filename>/range')
def range_request(filename):
    range_header = request.headers.get('Range', None)
    path = os.path.join(FILES_DIR, filename)

    if not range_header:
        return send_from_directory(FILES_DIR, filename)
    
    start, end = range_header.replace('bytes=', '').split('-')
    start = int(start)
    end = int(end) if end else None

    return generate_range_response(path, start, end)


print("\x1bc\x1b[47;34m")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

