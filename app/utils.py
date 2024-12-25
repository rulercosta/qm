def format_date_with_ordinal(date):
    day = date.day
    month = date.strftime('%B')
    year = date.strftime('%Y')

    # Determine the ordinal suffix
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    return f"{day}{suffix} {month}, {year}"
