# import os
# from dotenv import load_dotenv
# import requests
# import json

# # Load environment variables
# load_dotenv()

# def mock_response(prompt):
#     return f"(MOCK) Generated for prompt: {prompt}\n\nThis is sample content. Edit as needed."

# use_gemini = False
# GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
# working_model = None

# if GEMINI_KEY:
#     print(f"✅ API Key found: {GEMINI_KEY[:10]}...{GEMINI_KEY[-4:]}")
    
#     # Use the best available models (from your list)
#     # These are ordered by preference: fastest and most reliable first
#     test_models = [
#         "gemini-2.5-flash",        # Fast and efficient
#         "gemini-2.0-flash",         # Stable alternative
#         "gemini-2.5-pro",           # More capable but slower
#         "gemini-flash-latest",      # Fallback to latest
#     ]
    
#     for model_name in test_models:
#         try:
#             url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
#             response = requests.post(
#                 url,
#                 headers={"Content-Type": "application/json"},
#                 json={
#                     "contents": [{
#                         "parts": [{"text": "Say OK"}]
#                     }]
#                 },
#                 timeout=10
#             )
            
#             if response.status_code == 200:
#                 working_model = model_name
#                 use_gemini = True
#                 print(f"✅ Gemini Enabled Successfully with model: {model_name}")
#                 break
#             else:
#                 print(f"⚠️ Model {model_name} failed: {response.status_code}")
#         except Exception as e:
#             print(f"⚠️ Model {model_name} error: {str(e)[:100]}")
    
#     if not use_gemini:
#         print("❌ Could not connect to any Gemini model")
# else:
#     print("❌ No GEMINI_API_KEY found in environment")


# def call_gemini_api(prompt):
#     """Call Gemini API directly via HTTP"""
#     if not use_gemini or not working_model:
#         return None
    
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/{working_model}:generateContent?key={GEMINI_KEY}"
    
#     payload = {
#         "contents": [{
#             "parts": [{"text": prompt}]
#         }],
#         "generationConfig": {
#             "temperature": 0.7,
#             "maxOutputTokens": 2048,
#         }
#     }
    
#     try:
#         response = requests.post(
#             url,
#             headers={"Content-Type": "application/json"},
#             json=payload,
#             timeout=30
#         )
        
#         if response.status_code == 200:
#             data = response.json()
#             text = data['candidates'][0]['content']['parts'][0]['text']
#             return text
#         else:
#             print(f"❌ API Error {response.status_code}: {response.text[:200]}")
#             return None
            
#     except Exception as e:
#         print(f"❌ Exception calling Gemini: {e}")
#         return None


# def generate_section_content(title, topic):
#     """Generate content for a section using Gemini API"""
#     prompt = f"""Write a clear, well-structured section about the following topic.

# Section Title: {title}
# Main Topic: {topic}

# Requirements:
# - Write approximately 200-250 words
# - Use professional tone
# - Include relevant details and examples
# - Format with proper paragraphs

# Please provide the content now:"""

#     if use_gemini:
#         print(f"🔄 Generating content for: {title}")
#         result = call_gemini_api(prompt)
        
#         if result:
#             print(f"✅ Content generated successfully for: {title}")
#             return result
#         else:
#             print(f"⚠️ API call failed, using mock response")
#             return mock_response(prompt)
#     else:
#         print("⚠️ Using mock response (Gemini not available)")
#         return mock_response(prompt)


# def refine_content(old_text, instruction):
#     """Refine existing content based on user instruction"""
    
#     # Special handling for REPLACE_WITH instruction
#     if instruction.startswith("REPLACE_WITH: "):
#         return instruction.replace("REPLACE_WITH: ", "")
    
#     prompt = f"""Please refine the following text according to the instruction provided.

# Instruction: {instruction}

# Original Text:
# {old_text}

# Please provide the refined version:"""

#     if use_gemini:
#         print(f"🔄 Refining content with instruction: {instruction[:50]}...")
#         result = call_gemini_api(prompt)
        
#         if result:
#             print(f"✅ Content refined successfully")
#             return result
#         else:
#             print(f"⚠️ API call failed, using mock response")
#             return mock_response(prompt)
#     else:
#         print("⚠️ Using mock response (Gemini not available)")
#         return mock_response(prompt)


import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

def mock_response(prompt):
    return f"(MOCK) Generated for prompt: {prompt}\n\nThis is sample content. Edit as needed."

use_gemini = False
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
working_model = None

if GEMINI_KEY:
    print(f"✅ API Key found: {GEMINI_KEY[:10]}...{GEMINI_KEY[-4:]}")
    
    test_models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.5-pro",
        "gemini-flash-latest",
    ]
    
    for model_name in test_models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": "Say OK"}]
                    }]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                working_model = model_name
                use_gemini = True
                print(f"✅ Gemini Enabled Successfully with model: {model_name}")
                break
            else:
                print(f"⚠️ Model {model_name} failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Model {model_name} error: {str(e)[:100]}")
    
    if not use_gemini:
        print("❌ Could not connect to any Gemini model")
else:
    print("❌ No GEMINI_API_KEY found in environment")


def call_gemini_api(prompt):
    """Call Gemini API directly via HTTP"""
    if not use_gemini or not working_model:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{working_model}:generateContent?key={GEMINI_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048,
        }
    }
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            text = data['candidates'][0]['content']['parts'][0]['text']
            return text
        else:
            print(f"❌ API Error {response.status_code}: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Exception calling Gemini: {e}")
        return None


def generate_section_content(title, topic):
    """Generate content for a section using Gemini API"""
    prompt = f"""Write a clear, well-structured section about the following topic.

Section Title: {title}
Main Topic: {topic}

Requirements:
- Write approximately 200-250 words
- Use professional tone
- Include relevant details and examples
- Format with proper paragraphs

Please provide the content now:"""

    if use_gemini:
        print(f"📄 Generating content for: {title}")
        result = call_gemini_api(prompt)
        
        if result:
            print(f"✅ Content generated successfully for: {title}")
            return result
        else:
            print(f"⚠️ API call failed, using mock response")
            return mock_response(prompt)
    else:
        print("⚠️ Using mock response (Gemini not available)")
        return mock_response(prompt)


def refine_content(old_text, instruction):
    """Refine existing content based on user instruction"""
    
    if instruction.startswith("REPLACE_WITH: "):
        return instruction.replace("REPLACE_WITH: ", "")
    
    prompt = f"""Please refine the following text according to the instruction provided.

Instruction: {instruction}

Original Text:
{old_text}

Please provide the refined version:"""

    if use_gemini:
        print(f"📄 Refining content with instruction: {instruction[:50]}...")
        result = call_gemini_api(prompt)
        
        if result:
            print(f"✅ Content refined successfully")
            return result
        else:
            print(f"⚠️ API call failed, using mock response")
            return mock_response(prompt)
    else:
        print("⚠️ Using mock response (Gemini not available)")
        return mock_response(prompt)


def generate_outline(topic, doc_type):
    """
    NEW FEATURE: AI-Generated outline/template suggestion
    Returns list of section/slide titles based on topic
    """
    if doc_type == "docx":
        prompt = f"""Generate a professional document outline for the following topic: "{topic}"

Provide 5-8 section headings that would make a comprehensive document. 
Return ONLY a JSON array of strings, nothing else. No markdown, no explanations.

Example format: ["Introduction", "Background", "Analysis", "Conclusion"]

Your response:"""
    else:  # pptx
        prompt = f"""Generate a professional PowerPoint presentation outline for the following topic: "{topic}"

Provide 6-10 slide titles that would make a comprehensive presentation.
Return ONLY a JSON array of strings, nothing else. No markdown, no explanations.

Example format: ["Title Slide", "Overview", "Key Points", "Data Analysis", "Conclusion"]

Your response:"""

    if use_gemini:
        print(f"🤖 Generating AI outline for: {topic}")
        result = call_gemini_api(prompt)
        
        if result:
            try:
                # Clean up response (remove markdown if present)
                clean_result = result.strip()
                if clean_result.startswith("```json"):
                    clean_result = clean_result.replace("```json", "").replace("```", "").strip()
                elif clean_result.startswith("```"):
                    clean_result = clean_result.replace("```", "").strip()
                
                outline = json.loads(clean_result)
                
                if isinstance(outline, list) and len(outline) > 0:
                    print(f"✅ Generated {len(outline)} sections/slides")
                    return outline
                else:
                    print("⚠️ Invalid outline format, using fallback")
                    return generate_fallback_outline(topic, doc_type)
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parse error: {e}, using fallback")
                return generate_fallback_outline(topic, doc_type)
        else:
            print("⚠️ API failed, using fallback outline")
            return generate_fallback_outline(topic, doc_type)
    else:
        print("⚠️ Gemini not available, using fallback outline")
        return generate_fallback_outline(topic, doc_type)


def generate_fallback_outline(topic, doc_type):
    """Fallback outline when AI is unavailable"""
    if doc_type == "docx":
        return [
            "Introduction",
            f"Background on {topic}",
            "Key Analysis",
            "Findings and Discussion",
            "Conclusion"
        ]
    else:  # pptx
        return [
            f"{topic} - Overview",
            "Background",
            "Key Points",
            "Data and Analysis",
            "Insights",
            "Recommendations",
            "Conclusion"
        ]