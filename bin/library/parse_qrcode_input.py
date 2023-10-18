def parse_qrcode_input():
    qrcode = input("Mungo ID or QR Code: ")
    if qrcode == "*":
        exit()
    if qrcode.startswith("https://joeeasterly.github.io/go/"):
        qrcode = qrcode.replace("https://joeeasterly.github.io/go/", "")
    return qrcode