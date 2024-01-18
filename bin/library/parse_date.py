def parse_date(message = None):
    try:
        from dateparser import parse
    #handling exception if file not found
    except ImportError as err:
        print("Error>>", err)
    
    if message == None:
        message = "Enter date: "

    input_date = input(message)

    # if input is eight consecutive digits, parse as YYYYMMDD
    if input_date.isdigit() and len(input_date) == 8:
        output_date = parse(input_date, date_formats=["%Y%m%d"])
    else:
        output_date = parse(input_date)
    return str(output_date)