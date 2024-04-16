import numpy as np
import torch
import torchvision.transforms as T
from transformers import AutoFeatureExtractor, AutoModel

threshold_unique = 0.72


class UniqueSearchModel:
    def __init__(self):
        model_ckpt = "google/vit-base-patch16-224-in21k"
        extractor = AutoFeatureExtractor.from_pretrained(model_ckpt)
        self.model = AutoModel.from_pretrained(model_ckpt)
        self.hidden_dim = self.model.config.hidden_size

        self.transformation_chain = T.Compose(
            [
                # We first resize the input image to 256x256 and then we take center crop.
                T.Resize(int((256 / 224) * extractor.size["height"])),
                T.CenterCrop(extractor.size["height"]),
                T.ToTensor(),
                T.Normalize(mean=extractor.image_mean, std=extractor.image_std),
            ]
        )

    def _compute_scores(self, emb_one, emb_two):
        """Computes cosine similarity between two vectors."""
        scores = torch.nn.functional.cosine_similarity(emb_one, emb_two)
        return scores.numpy().tolist()

    def _get_embedding(self, image):
        transformed_image = self.transformation_chain(image).unsqueeze(0)
        new_batch = {"pixel_values": transformed_image.to(self.model.device)}
        # Commute the embedding.
        with torch.no_grad():
            embedding = self.model(**new_batch).last_hidden_state[:, 0].cpu()

        return embedding

    # def _extract_embeddings(model: torch.nn.Module):
    #     """Utility to compute embeddings."""
    #
    #     def pp(batch):
    #         images = batch["image"]
    #         image_batch_transformed = torch.stack(
    #             [transformation_chain(image) for image in images]
    #         )
    #         new_batch = {"pixel_values": image_batch_transformed.to(device)}
    #         with torch.no_grad():
    #             embeddings = model(**new_batch).last_hidden_state[:, 0].cpu()
    #         return {"embeddings": embeddings}
    #
    #     return pp
    #
    # # Here, we map embedding extraction utility on our subset of candidate images.
    # batch_size = 24
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # extract_fn = _extract_embeddings(model.to(device))
    # candidate_subset_emb = train_dataset.map(extract_fn, batched=True, batch_size=batch_size)
    #
    # candidate_ids = []
    #
    # for id in tqdm(range(len(candidate_subset_emb))):
    #     label = candidate_subset_emb[id]["label"]
    #
    #     # Create a unique indentifier.
    #     entry = str(id) + "_" + str(label)
    #
    #     candidate_ids.append(entry)
    #
    # all_candidate_embeddings = np.array(candidate_subset_emb["embeddings"])
    # all_candidate_embeddings = torch.from_numpy(all_candidate_embeddings)
    #
    # def _get_similarity_mapping(image):
    #     # Compute similarity scores with all the candidate images at one go.
    #     # We also create a mapping between the candidate image identifiers
    #     # and their similarity scores with the query image.
    #     sim_scores = compute_scores(all_candidate_embeddings, get_embedding(image))
    #     # print(sim_scores)
    #     similarity_mapping = dict(zip(candidate_ids, sim_scores))
    #     return similarity_mapping
    #
    # def fetch_similar(self, image, top_k=5):
    #     similarity_mapping = self._get_similarity_mapping(image)
    #
    #     # Sort the mapping dictionary and return `top_k` candidates.
    #     similarity_mapping_sorted = dict(
    #         sorted(similarity_mapping.items(), key=lambda x: x[1], reverse=True)
    #     )
    #     id_entries = list(similarity_mapping_sorted.keys())[:top_k]
    #     ids = list(map(lambda x: int(x.split("_")[0]), id_entries))
    #     labels = list(map(lambda x: int(x.split("_")[-1]), id_entries))
    #     return ids, labels

    def is_duplicate(self, image1, image2):
        emb_one = self._get_embedding(image1)
        emb_two = self._get_embedding(image2)
        print(self._compute_scores(emb_one, emb_two)[0] >= threshold_unique)
