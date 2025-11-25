import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

print("=" * 60)
print("GEMINI API KEY TESTER")
print("=" * 60)

if not GEMINI_KEY:
    print("❌ No GEMINI_API_KEY found in .env file")
    exit(1)

print(f"✅ API Key found: {GEMINI_KEY[:10]}...{GEMINI_KEY[-4:]}")
print()

# Test different API endpoints and models
test_cases = [
    {
        "name": "Gemini Pro (v1beta)",
        "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}",
        "payload": {
            "contents": [{
                "parts": [{"text": "Say hello"}]
            }]
        }
    },
    {
        "name": "Gemini 1.5 Flash (v1beta)",
        "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}",
        "payload": {
            "contents": [{
                "parts": [{"text": "Say hello"}]
            }]
        }
    },
    {
        "name": "Gemini Pro (v1)",
        "url": f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_KEY}",
        "payload": {
            "contents": [{
                "parts": [{"text": "Say hello"}]
            }]
        }
    }
]

working_models = []

for test in test_cases:
    print(f"Testing: {test['name']}")
    print(f"URL: {test['url'][:80]}...")
    
    try:
        response = requests.post(
            test['url'],
            headers={"Content-Type": "application/json"},
            json=test['payload'],
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            try:
                text = data['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ SUCCESS! Response: {text[:50]}")
                working_models.append(test['name'])
            except:
                print(f"✅ API responded but unexpected format")
                print(f"Response: {json.dumps(data, indent=2)[:200]}")
        else:
            print(f"❌ FAILED - Status Code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)[:300]}")
            except:
                print(f"Error: {response.text[:300]}")
    
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)[:200]}")
    
    print("-" * 60)
    print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)

if working_models:
    print(f"✅ {len(working_models)} working model(s) found:")
    for model in working_models:
        print(f"   - {model}")
    print()
    print("✅ Your API key is VALID and working!")
else:
    print("❌ No working models found")
    print()
    print("Possible issues:")
    print("1. API key may be invalid or expired")
    print("2. API key may not have proper permissions")
    print("3. Billing may not be enabled for your Google Cloud project")
    print()
    print("Next steps:")
    print("1. Visit https://aistudio.google.com/app/apikey")
    print("2. Generate a new API key")
    print("3. Update your .env file with the new key")