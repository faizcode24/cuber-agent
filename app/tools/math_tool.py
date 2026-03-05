import re

def calculate_cagr(query: str):
    nums = list(map(int, re.findall(r'\d+', query)))
    start, end, years = nums[:3]
    cagr = ((end/start)**(1/years)-1)*100
    return round(cagr, 2)
