def validate(card):
    card_no = str(card)
    card_length = ''
    card_prefixes = {
        '4': 'Visa',
        '5': 'Mastercard',
        '37': 'American Express',
        '6': 'Discover'
    }

    for prefix, card_type in card_prefixes.items():
        if card_no.startswith(prefix):
            card_length = card_type
            break

    if not card_length or len(card_no) not in [13, 15, 16]:
        return "Invalid card length or prefix"

    total_sum = 0
    for i, digit in enumerate(card_no):
        if i % 2 == 0:
            multiplied = int(digit) * 2
            total_sum += sum(int(d) for d in str(multiplied))
        else:
            total_sum += int(digit)
    print(total_sum)

    if total_sum % 10 == 0:
        return f"The provided {card_length} card is valid"
    else:
        return "The card is not valid"

    



card = int(5036000000000007)
print(validate(card))