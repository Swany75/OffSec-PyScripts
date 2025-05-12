#!/usr/bin/env python3

from modules.my_utils import show_message

### Functions ########################################################################################################################

def response(packet):
    
    content_type = packet.response.headers.get("content-type", "")

    try:
        if "image" in content_type:
            url = packet.request.url
            extension = content_type.split("/")[-1]

            if extension == "jpeg":
                extension = "jpg"

            file_name = f"images/{url.replace('/', '_').replace(':', '_')}.{extension}"
            image_data = packet.response.content

            with open(file_name, "wb") as f:
                f.write(image_data)

            show_message("Imagen guardada:", "", file_name)

    except:
        pass

### Main Code #######################################################################################################################

def main():
    try:
        from mitmproxy import http
    
    except ImportError as e:
        show_message("Executa:", "error", "mitmproxy/mitmdump -s image_sniffer.py --quiet")
        return

if __name__ == "__main__":
    main()
