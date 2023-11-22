from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def translate_text(input_text):
    # Replace "your-username/your-model-name" with the correct username and model name
    model_name = "AbbyMuso1/model_trans_lu_sw_3"

    # Load model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenize input text
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Generate translation
    translated_ids = model.generate(input_ids)
    translated_text = tokenizer.batch_decode(translated_ids, skip_special_tokens=True)[0]

    return translated_text
