#!/usr/bin/python

def try_to_num2words(Word, L):
    try:
        N = int(Word)
        Expanded = simple_num2words(N, L)
        if Expanded:
            return Expanded
        else:
            return Word  
    except ValueError:
       return Word
    
def simple_num2words(N, L):
    if L == 'english':
        return num2words_en(N)
    elif L == 'french':
        return num2words_fr(N)
    elif L == 'german':
        return num2words_de(N)
    else:
        return False

# ====================================================================

def num2words_en(N):
    if under_20(N):
        return english(N)
    elif tens_number(N):
        return english(N)
    elif under_100(N):
        return english(int( N - N % 10 )) + ' ' + english(N % 10 )
    elif hundreds_number(N):
        return num2words_en(int( N / 100 )) + ' ' + english(100)
    elif under_1000(N):
        return num2words_en(int( N / 100 )) + ' ' + english(100) +  ' and ' + num2words_en(N % 100 )

english_base = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
                6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
                11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
                16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
                20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty',
                60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety',
                100: 'hundred', 1000: 'thousand'}

def english(N):
    global english_base
    if N in english_base:
        return english_base[N]
    else:
        return N

# ====================================================================

# Actually Swiss French numbers

def num2words_fr(N):
    if under_20(N):
        return french(N)
    elif N == 80:
        return 'quatre-vingts'
    elif tens_number(N):
        return french(N)
    elif N == 81:
        return 'quatre-vingt un'
    elif under_100(N) and N % 10 == 1:
        return french(int( N - N % 10 )) + ' et un' 
    elif under_100(N):
        return french(int( N - N % 10 )) + ' ' + french(N % 10 )
    elif N == 100:
        return 'cent'
    elif hundreds_number(N):
        return num2words_fr(int( N / 100 )) + ' ' + french(100)
    elif under_1000(N):
        return num2words_fr(N - N % 100) + ' ' + num2words_fr(N % 100 )

french_base =  {1: 'un', 2: 'deux', 3: 'trois', 4: 'quatre', 5: 'cinq',
                6: 'six', 7: 'sept', 8: 'huit', 9: 'neuf', 10: 'dix',
                11: 'onze', 12: 'douze', 13: 'treize', 14: 'quatorze', 15: 'quinze',
                16: 'seize', 17: 'dix-sept', 18: 'dix-huit', 19: 'dix-neuf',
                20: 'vingt', 30: 'trente', 40: 'quarante', 50: 'cinquante',
                60: 'soixante', 70: 'septante', 80: 'quatre-vingt', 90: 'nonante',
                100: 'cent', 1000: 'mille'}

def french(N):
    global french_base
    if N in french_base:
        return french_base[N]
    else:
        return N
    
# ====================================================================

def num2words_de(N):
    if under_20(N):
        return german(N)
    elif tens_number(N):
        return german(N)
    elif under_100(N):
        return german(N % 10 ) + ' und ' + german(int( N - N % 10 )) 
    elif N == 100:
        return 'ein hundert'
    elif hundreds_number(N):
        return num2words_de(int( N / 100 )) + ' ' + german(100)
    elif under_1000(N):
        return num2words_de(N - N % 100) + ' ' + num2words_de(N % 100)

german_base = {1: 'eins', 2: 'zwei', 3: 'drei', 4: 'vier', 5: 'fünf',
                6: 'sechs', 7: 'sieben', 8: 'acht', 9: 'neun', 10: 'zehn',
                11: 'elf', 12: 'zwölf', 13: 'dreizehn', 14: 'vierzehn', 15: 'fünfzehn',
                16: 'sechzehn', 17: 'siebzehn', 18: 'achtzehn', 19: 'neunzehn',
                20: 'zwanzig', 30: 'dreiβig', 40: 'vierzig', 50: 'fünfzig',
                60: 'sechzig', 70: 'siebzig', 80: 'achtzig', 90: 'neunzig',
                100: 'hundert', 1000: 'thousand'}

def german(N):
    global german_base
    if N in german_base:
        return german_base[N]
    else:
        return N

# ====================================================================

def under_20(N):
    return N <= 20

def tens_number(N):
    return N <= 99 and N % 10 == 0

def under_100(N):
    return N <= 99

def hundreds_number(N):
    return N <= 999 and N % 100 == 0

def under_1000(N):
    return N <= 999
        
