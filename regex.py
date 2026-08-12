import re

# .       — будь-який символ, крім нового рядка (якщо не увімкнено DOTALL)
# ^ $     — початок / кінець рядка (з MULTILINE — початок/кінець кожного рядка)
# \d \D   — цифра / не-цифра;  \w \W — «словесний» символ / ні;  \s \S — пробільний / ні
# [abc]   — один символ з переліку;  [^abc] — один символ НЕ з переліку
# |       — альтернатива (або ліва, або права частина)
# ()      — група захоплення (підрядок можна витягти через .group(1) або ім'я)
# (?:...) — група без захоплення (лише для структури шаблону)
# * + ?   — 0+, 1+, 0 або 1 повторів;  {n} {n,} {n,m} — точна кількість повторів

# text_dot = "a\nbcdeaf"
# pattern = r"a."
# print(re.findall(pattern, text_dot))


text_star = "ab, a, aab, ac, abbbbbcbbbb"
pattern = r"ab*"
print(re.findall(pattern, text_star))

text_plus = "ab, a, aab, ac, abbbbbcbbbb"
pattern = r"ab+"
print(re.findall(pattern, text_plus))


text_quantifiers = "color, colour, colar"
pattern = r"colou?r"
print(re.findall(pattern, text_quantifiers))


text_num = "123       abc45 678912"
pattern = r"\d{3}"
print(re.findall(pattern, text_num))

text_num = "123       abc45 678912"
pattern = r"\w{3,5}"
print(re.findall(pattern, text_num))

text_num = "123       abc45 678912"
pattern = r"\s{3,}"
print(re.findall(pattern, text_num))

text = "abcdabe"
pattern = r"[abcf]"
print(re.findall(pattern, text))

text = "abcdabe"
pattern = r"[^abcf]"
print(re.findall(pattern, text))


text = "grey, gray"
pattern = r"gr(a|e)y"
print(re.findall(pattern, text))


text = "grey, gray"
pattern = r"gr(?:a|e)y"
print(re.findall(pattern, text))

text = "grey, gray"
pattern = r"grey|gray"
print(re.findall(pattern, text))


text_date = "Date: 2026-08-12"
pattern = r"(\d{4})-(\d{2})-(\d{2})"
match = re.search(pattern, text_date)
if match:
    year, month, day = match.groups()
    print("Year:", year, "Month:", month, "Day:", day)

text = "Lorem Ipsum is simply dummy 12.34,56.78 text of the printing and typesetting industry.13.34,    46.78 Lorem Ipsum has been the industry's standard dummy text ever12.3 92.78 since 1966, when designers at Letraset and James Mosley"
pattern = r"(\d+\.\d+),?\s*(\d+\.\d+)"
match = re.findall(pattern, text)
print(match)
pos = 0

while match := re.search(pattern, text[pos:]):
    lat, lon = match.groups()
    print(lat, lon)
    pos += match.end()

text = "apple, banana;        orange.pear"
pattern = r"[,;\.]\s*"
print(re.split(pattern, text))

text = "123-456-7890"
pattern_verbose = re.compile("""
    ^                   #Start number
    (?P<area_code>\\d{3})             #3 digits
    [\\s-]?
    (?P<number>\\d{3}-\\d{4})       #3 digits - 4 digits
    $
""", re.VERBOSE)
match = pattern_verbose.search(text)
if match:
    print(f"Code: {match.group("area_code")} Number: {match.group('number')}")


samples = [
    "+38 (067) 123-45-67",
    "0671234567",
    "+380671234567"
]

pattern = re.compile(r"""
    ^
    (?P<country>\+\d{2})?
    [\s]*
    (?P<number>\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})
    $
    
""", re.VERBOSE)

for sample in samples:
    print('='*50)
    m = pattern.search(sample)
    if m:
        print(f"sample: {sample} \nCountry: {m.group("country")}\nNumber: {m.group('number')}")
    else:
        print(f"Pattern doesnt match: {sample}")