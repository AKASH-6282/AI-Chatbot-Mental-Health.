from flask import Flask, request, jsonify
from transformers import (
    AutoModelForSequenceClassification,
    AutoModelForCausalLM,
    AutoTokenizer,
)
import torch
from safety import is_safe, crisis_detected, sanitize_text

app = Flask(__name__)

# -------------------------------------------
# Load Emotion Classification Model
# -------------------------------------------
try:
    emotion_model_name = "fine_tuned_model"
    emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
    emotion_model = AutoModelForSequenceClassification.from_pretrained(
        emotion_model_name
    )
    print("✅ Emotion model loaded.")
except Exception as e:
    print("❌ Error loading emotion model:", e)
    raise e

# -------------------------------------------
# Load Chat Model
# -------------------------------------------
try:
    chat_model_name = "gpt2"
    chat_tokenizer = AutoTokenizer.from_pretrained(chat_model_name)
    chat_model = AutoModelForCausalLM.from_pretrained(chat_model_name)
    print("✅ Chatbot model loaded.")
except Exception as e:
    print("❌ Error loading chat model:", e)
    raise e

# -------------------------------------------
# Emotion Detection
# -------------------------------------------
def detect_emotion(text):
    tokens = emotion_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = emotion_model(**tokens).logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class

# -------------------------------------------
# Chat Route
# -------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_msg = data["message"]
    clean_input = sanitize_text(user_msg)

    # -------------------------
    # Crisis detection
    # -------------------------
    if crisis_detected(clean_input):
        return jsonify({
            "reply": (
                "I'm really sorry you're feeling this way. Please reach out to a trained professional:\n"
                "📞 Suicide Hotline India: 9152987821\n"
                "📞 Aasra Helpline: +91 9820466726\n"
                "You are not alone."
            )
        })

    # -------------------------
    # Safety check
    # -------------------------
    if not is_safe(clean_input):
        return jsonify({"reply": "Please avoid harmful or offensive language."})

    # -------------------------
    # Emotion detection
    # -------------------------
    emotion_id = detect_emotion(clean_input)

    emotion_prompts = {
        0: "The user seems sad. Respond with empathy and warmth.",
        1: "The user is feeling joy. Respond positively and supportively.",
        2: "The user is angry. Reply calmly and help them feel heard.",
        3: "The user is fearful. Reply with reassurance and safety.",
        4: "The user is surprised. Respond gently and thoughtfully.",
        5: "The user feels love or affection. Respond kindly.",
    }

    emotion_context = emotion_prompts.get(emotion_id, "")

    # -------------------------
    # SYSTEM PROMPT (Prevents repetition)
    # -------------------------
    SYSTEM_PROMPT = (
        "You are a supportive mental health assistant. "
        "You reply with empathy and helpful guidance. "
        "Do NOT repeat the user's input. "
        "Keep responses short, warm, and comforting."
    )

    # -------------------------
    # Final Prompt
    # -------------------------
    prompt = (
        f"{SYSTEM_PROMPT}\n"
        f"{emotion_context}\n"
        f"User: {clean_input}\n"
        f"Assistant:"
    )

    inputs = chat_tokenizer(prompt, return_tensors="pt")

    # -------------------------
    # Generate response
    # -------------------------
    output = chat_model.generate(
        **inputs,
        max_length=100,
        temperature=0.7,
        top_p=0.9,
        no_repeat_ngram_size=4,
        pad_token_id=chat_tokenizer.eos_token_id,
        do_sample=True,
        eos_token_id=chat_tokenizer.eos_token_id
    )

    reply = chat_tokenizer.decode(output[0], skip_special_tokens=True)
    reply = reply.replace(prompt, "").strip()  # remove prompt text

    return jsonify({"reply": reply})

# -------------------------------------------
# Run App
# -------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

