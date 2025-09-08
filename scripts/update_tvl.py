#!/usr/bin/env python3

import requests
import json
import re
from datetime import datetime

def fetch_tvl_data():
    """Fetch TVL data from Yala API"""
    try:
        response = requests.get('https://public.yala.org:2053/public/yalaProtocol', timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['data']
    except Exception as e:
        print(f"Error fetching TVL data: {e}")
        return None

def format_tvl(tvl):
    """Format TVL value to readable format"""
    if tvl >= 1e9:
        return f"${tvl/1e9:.2f}B"
    elif tvl >= 1e6:
        return f"${tvl/1e6:.2f}M"
    elif tvl >= 1e3:
        return f"${tvl/1e3:.2f}K"
    else:
        return f"${tvl:.2f}"

def update_readme(data):
    """Update README.md with new TVL data"""
    if not data:
        return
    
    tvl = data.get('tvl', 0)
    tvl_formatted = format_tvl(tvl)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    
    # Read README
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Create the new Yala line with TVL
    new_line = f"- **Yala** - Launched [Yala](https://yala.org), the liquidity layer for Bitcoin **TVL: {tvl_formatted}** *(Updated: {timestamp})*"
    
    # Replace the Yala line
    pattern = r'- \*\*Yala\*\* - Launched \[Yala\]\(https://yala\.org\), the liquidity layer for Bitcoin.*'
    content = re.sub(pattern, new_line, content)
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(content)
    
    print(f"README updated with TVL: {tvl_formatted}")

if __name__ == "__main__":
    data = fetch_tvl_data()
    update_readme(data)