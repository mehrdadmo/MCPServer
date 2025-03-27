from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/process_revit_query', methods=['POST'])
def process_revit_query():
    try:
        data = request.get_json()
        
        # Extract request data
        prompt = data.get('prompt')
        model = data.get('model', 'claude-3-sonnet')
        revit_elements = data.get('revit_elements')
        project_info = data.get('project_info')

        # Construct the system prompt
        system_prompt = """You are an expert in Autodesk Revit and architectural design. 
        Analyze the provided information and suggest appropriate actions or modifications."""
        
        # Combine project info and elements with user prompt
        context = f"""
        Project Information: {project_info}
        Revit Elements: {revit_elements}
        User Query: {prompt}
        """

        # Call Claude API
        message = anthropic.messages.create(
            model=model,
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": context}
            ]
        )

        # Process the response
        suggested_actions = extract_suggested_actions(message.content)

        return jsonify({
            "response": message.content,
            "suggested_actions": suggested_actions,
            "error": None
        })

    except Exception as e:
        return jsonify({
            "response": None,
            "suggested_actions": [],
            "error": str(e)
        }), 500

def extract_suggested_actions(response: str) -> List[str]:
    # Implement logic to extract actionable items from Claude's response
    # This is a placeholder implementation
    return ["Action 1", "Action 2"]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 