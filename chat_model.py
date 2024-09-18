import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from config import MODEL_NAME


class ChatModel:
    def __init__(self, access_token):
        if torch.cuda.is_available():
            device = 'cuda'
        elif torch.backends.mps.is_available():
            device = 'mps'
        else:
            device = 'cpu'

        self.device = torch.device(device)

        model_name = MODEL_NAME

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=access_token
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map='auto',
            load_in_4bit=True if device == 'cuda' else False,
            token=access_token
        )
        self.model.to(self.device)

    def get_device_type(self):
        return self.device.type

    def generate_response(self, system_prompt, user_prompt):
        full_prompt = f"""[INST] <<SYS>>
        {system_prompt}
        <</SYS>>
        
        {user_prompt} [/INST]
        """

        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                do_sample=True,
                top_k=10,
                top_p=0.9,
                temperature=0.3,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        generated_text = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
        return generated_text
