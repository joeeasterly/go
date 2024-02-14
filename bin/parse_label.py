from get_last_record import get_last_record
def parse_label(existing_label = None):
    last_label = get_last_record().get('label', None)
    permitted_characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                            "u", "v", "w", "x", "y", "z",
                            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                            "U", "V", "W", "X", "Y", "Z", 
                            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                            "-", "_", " ", ".", ",", "!", "@", "#", "$", "%",
                            "^", "&"]
    label_prompt = "Enter Label: "
    if existing_label:
        label_prompt = f"Enter Label [{existing_label}]: "
    label = input(label_prompt)
    if not label:
        label = existing_label
    if label == "+":
        label = last_label
    # Remove all characters in the label except those in the permitted_characters list.
    label = "".join([character for character in label if character in permitted_characters])
    return label