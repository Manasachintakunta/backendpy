from flask import Flask, request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(_name_)

# Load the T5 model and tokenizer from Hugging Face
model_name = "t5-small"  # You can choose a larger version if needed
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Tokenize the user input and generate a response
    input_text = f"question: {user_message} </s>"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate a response from the model
    output_ids = model.generate(input_ids, max_length=100, num_beams=4, early_stopping=True)
    response_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return jsonify({"response": response_text})

if _name_ == '_main_':
    app.run(debug=True)