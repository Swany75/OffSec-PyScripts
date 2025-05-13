from mitmproxy import http

def response(flow: http.HTTPFlow):
    # Només actuem si el contingut és HTML
    if "text/html" in flow.response.headers.get("content-type", ""):
        # Assegurem que tenim accés a les dades
        html = flow.response.text
        
        # Codi que volem injectar (pots posar qualsevol script)
        inject_code = '<script>alert("Pàgina interceptada!");</script>'

        # L'injectem abans de </body> (millor per evitar errors visuals)
        modified_html = html.replace("</body>", inject_code + "</body>")
        
        flow.response.text = modified_html
