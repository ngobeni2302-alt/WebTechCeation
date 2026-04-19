import qrcode
import os
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
save_path = os.path.join(root_dir, "website_qr.png")

# Auto-detect IP and use port 8080 (from server.py/open_web.sh)
local_ip = get_ip()
url = f"http://{local_ip}:8080"

print(f"Detecting local network IP... Found: {local_ip}")
print(f"Generating QR code for: {url}")
print("NOTE: Make sure your phone is on the same Wi-Fi as this computer!")

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create and save image
img = qr.make_image(fill_color="black", back_color="white")
img.save(save_path)

print(f"Success! QR code saved to: {save_path}")
