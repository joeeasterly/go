def parse_qrcode_input():
    qrcode = input("Mungo ID (blank to auto-assign): ")
    if qrcode.startswith("https://joeeasterly.github.io/go/"):
        qrcode = qrcode.replace("https://joeeasterly.github.io/go/", "")
    return qrcode