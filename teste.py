def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(int(number/10) != 0):
            print(number)
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits