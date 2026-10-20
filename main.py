import http.server
import socketserver
import json
import urllib.parse
import webbrowser
import sys
import os

from backend.predict import race_strategy, track_lengths


PORT = 8080

class F1StrategyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/predict'):
            parsed_url = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed_url.query)
            
            track = params.get('track', ['Abu Dhabi Grand Prix'])[0]
            safety = int(params.get('safety', [2])[0])
            
            try:
                import backend.predict as predict
                
                top_strats, tyre_laps = predict.race_strategy(track, safety)

                response_data = {
                    "status": "success",
                    "strategies": top_strats,
                    "tyre_laps": tyre_laps,
                    "lap_len": predict.track_lengths[track]['len'],
                    "laps_total": predict.track_lengths[track]['laps'],
                    "country": predict.track_lengths[track]['country'],
                    "asphalt": predict.track_lengths[track]['asphalt'],
                    "climate": predict.track_lengths[track]['climate'],
                    "img_url": predict.track_lengths[track]['img']
                }
            except Exception as e:
                response_data = {"status": "error", "message": str(e)}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        clean_path = self.path.split('?')[0]
        
        if clean_path.endswith('.css'):
            try:
                import os
                file_path = clean_path.lstrip('/')
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/css; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                    return
            except Exception:
                pass

        return super().do_GET()

if __name__ == "__main__":
    handler = F1StrategyHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Гоночный комплекс F1 запущен на http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}/frontend/index.html")
        httpd.serve_forever()