from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

threshold = 0.59


class SimilarityModel:

    def __init__(self):
        self.sentence_predictor = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.image_to_text_predictor = pipeline("image-to-text", model="Abdou/vit-swin-base-224-gpt2-image-captioning")

        # self.tokenizer_en_ru = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
        # self.model_en_ru = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
        #
        # self.tokenizer_ru_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
        # self.model_ru_en = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")

    def _sentence_similarity(self, text1, text2):
        embedding_1 = self.sentence_predictor.encode(text1, convert_to_tensor=True)
        embedding_2 = self.sentence_predictor.encode(text2, convert_to_tensor=True)
        return util.cos_sim(embedding_1, embedding_2).item()

    def _image_to_text(self, image):
        result = self.image_to_text_predictor(image)
        return result[0]['generated_text']

    def _translate_en_ru(self, input="Input a text to translate"):
        return self._translate(input, self.tokenizer_en_ru, self.model_en_ru)

    def _translate_ru_en(self, input="Введите текст для перевода"):
        return self._translate(input, self.tokenizer_ru_en, self.model_ru_en)

    def _translate(input, tokenizer, model):
        input_ids = tokenizer.encode(input, return_tensors="pt")
        outputs = model.generate(input_ids, max_length=512)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Return True - if paint and task similar
    def compare_paint_and_task(self, paint, task, lang='en'):
        generated_text = self._image_to_text(paint)
        print(generated_text)
        if lang == 'ru':
            generated_text = self._translate_en_ru(generated_text)
        print(self._sentence_similarity(task, generated_text) > threshold)
