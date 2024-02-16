def parse_qrcode_input(input_message = "Mungo ID or QR Code: "):
    qrcode = input(input_message).lower()
    if qrcode == "*":
        qrcode = "exit_loop"
    if qrcode.startswith("https://joeeasterly.github.io/go/"):
        qrcode = qrcode.replace("https://joeeasterly.github.io/go/", "")
    return qrcode