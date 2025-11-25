import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

print("=" * 70)
print("LISTING ALL AVAILABLE GEMINI MODELS")
print("=" * 70)

if not GEMINI_KEY:
    print("❌ No GEMINI_API_KEY found in .env file")
    exit(1)

print(f"✅ API Key found: {GEMINI_KEY[:10]}...{GEMINI_KEY[-4:]}")
print()

# Try both API versions
api_versions = ["v1beta", "v1"]

for api_version in api_versions:
    print(f"\n{'='*70}")
    print(f"Testing API Version: {api_version}")
    print('='*70)
    
    url = f"https://generativelanguage.googleapis.com/{api_version}/models?key={GEMINI_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            if models:
                print(f"✅ Found {len(models)} models:\n")
                
                generate_models = []
                for model in models:
                    model_name = model.get('name', 'Unknown')
                    display_name = model.get('displayName', 'N/A')
                    supported_methods = model.get('supportedGenerationMethods', [])
                    
                    print(f"Model: {model_name}")
                    print(f"  Display Name: {display_name}")
                    print(f"  Supported Methods: {', '.join(supported_methods)}")
                    
                    # Check if it supports generateContent
                    if 'generateContent' in supported_methods:
                        generate_models.append(model_name)
                        print(f"  ✅ SUPPORTS generateContent")
                    else:
                        print(f"  ❌ Does NOT support generateContent")
                    print()
                
                if generate_models:
                    print("\n" + "="*70)
                    print("✅ MODELS THAT SUPPORT generateContent:")
                    print("="*70)
                    for m in generate_models:
                        # Extract just the model name without the 'models/' prefix
                        clean_name = m.replace('models/', '')
                        print(f"  - {clean_name}")
                    print()
                    print("Use one of these model names in your llm.py file!")
                else:
                    print("❌ No models support generateContent method")
            else:
                print("❌ No models returned")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Error: {response.text[:500]}")
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

print("\n" + "="*70)
print("TESTING COMPLETE")
print("="*70)