import torch
import torchvision.transforms as T
from PIL import Image
from transformers import AutoFeatureExtractor, AutoModel

threshold_unique = 0.72


def _compute_scores(emb_one, emb_two):
    """Computes cosine similarity between two vectors."""
    scores = torch.nn.functional.cosine_similarity(
        torch.FloatTensor(emb_one),
        torch.FloatTensor(emb_two),
        dim=0
    )
    return scores.numpy().tolist()


class UniqueSearchModel:
    def __init__(self):
        model_ckpt = "google/vit-base-patch16-224-in21k"
        self.extractor = AutoFeatureExtractor.from_pretrained(model_ckpt)
        self.model = AutoModel.from_pretrained(model_ckpt)

        self.transformation_chain = T.Compose(
            [
                # We first resize the input image to 256x256 and then we take center crop.
                T.Resize(int((256 / 224) * self.extractor.size["height"])),
                T.CenterCrop(self.extractor.size["height"]),
                T.ToTensor(),
                T.Normalize(mean=self.extractor.image_mean, std=self.extractor.image_std),
            ]
        )

        self.all_embeddings = dict()

    def extract_embedding(self, image):
        image_pp = self.extractor(image, return_tensors="pt")
        features = self.model(**image_pp).last_hidden_state[:, 0].detach().numpy()
        return features.squeeze()

    def _get_similarity_mapping(self, image):
        sim_scores = []
        query_embedding = self.extract_embedding(image)
        for embedding in self.all_embeddings.values():
            sim_scores.append(_compute_scores(embedding, query_embedding))
        similarity_mapping = dict(zip(self.all_embeddings.keys(), sim_scores))
        return similarity_mapping

    def start(self, images_ids):
        for image, id in images_ids:
            self.add_image(image, id)

    def add_image(self, image, id):
        self.all_embeddings[id] = self.extract_embedding(image)

    def remove_image(self, id):
        self.all_embeddings.pop(id)

    def fetch_similar(self, image, top_k=5):
        similarity_mapping = self._get_similarity_mapping(image)

        # Sort the mapping dictionary and return `top_k` candidates.
        similarity_mapping_sorted = dict(
            sorted(similarity_mapping.items(), key=lambda x: x[1], reverse=True)
        )
        id_entries = list(similarity_mapping_sorted.keys())[:top_k]
        return id_entries

    def find_duplicates(self, image):
        similarity_mapping = self._get_similarity_mapping(image)

        similarity_mapping_sorted = dict(
            sorted(similarity_mapping.items(), key=lambda x: x[1], reverse=True)
        )
        id_entries = [k for (k, v) in similarity_mapping_sorted.items() if v > threshold_unique]
        return id_entries


def test():
    unique_search = UniqueSearchModel()
    for i in range(1, 8):
        image = Image.open("./test_images/1/" + str(i) + ".jpg")
        unique_search.add_image(image, i + 10)
    for i in range(1, 8):
        image = Image.open("./test_images/2/" + str(i) + ".jpg")
        unique_search.add_image(image, i + 20)
    image_last = Image.open("test_images/2/8.jpg")
    print(unique_search.fetch_similar(image_last, 5))
    print(unique_search.find_duplicates(image_last))
