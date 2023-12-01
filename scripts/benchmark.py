import time

import torch
from transformers import pipeline

models = ["openai/whisper-large-v3", "distil-whisper/large-v2"]
test_flash_attention = [True, False]
device = "cuda:0"
batch_sizes = [1, 8, 16, 24]

file_name = (
    "https://huggingface.co/datasets/reach-vb/random-audios/resolve/main/ted_60.wav"
)

for model in models:
    for fa2 in test_flash_attention:
        for batch_size in batch_sizes:
            pipe = pipeline(
                "automatic-speech-recognition",
                model=model,
                torch_dtype=torch.float16,
                device=device,
                model_kwargs={"use_flash_attention_2": fa2},
            )
        if fa2 == False:
            pipe.model = pipe.model.to_bettertransformer()
        start = time.time()
        outputs = pipe(
            file_name,
            chunk_length_s=30,
            batch_size=batch_size,
            return_timestamps=True,
        )
        end = time.time()
        total_time = end - start
        print(total_time)
