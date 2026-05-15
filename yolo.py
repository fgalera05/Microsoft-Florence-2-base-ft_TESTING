from PIL import Image
import torch
import time
from transformers import AutoProcessor, AutoModelForCausalLM

IMAGEN = "yolo2.png"
MODEL_ID = "microsoft/Florence-2-base-ft"

inicio_total = time.perf_counter()

print("Iniciando...")
print(f"Modelo: {MODEL_ID}")
print(f"Imagen: {IMAGEN}")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Dispositivo: {device}")

print("Cargando modelo...")
t0 = time.perf_counter()

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
).to(device)

processor = AutoProcessor.from_pretrained(
    MODEL_ID,
    trust_remote_code=True
)

t1 = time.perf_counter()
print(f"Modelo cargado en {t1 - t0:.2f} segundos")

print("Abriendo imagen...")
t0 = time.perf_counter()

image = Image.open(IMAGEN).convert("RGB")

t1 = time.perf_counter()
print(f"Imagen abierta en {t1 - t0:.2f} segundos")
print(f"Tamaño imagen: {image.width}x{image.height}")

prompt = "<MORE_DETAILED_CAPTION>"

print("Preparando entrada...")
t0 = time.perf_counter()

inputs = processor(
    text=prompt,
    images=image,
    return_tensors="pt"
).to(device)

t1 = time.perf_counter()
print(f"Entrada preparada en {t1 - t0:.2f} segundos")

print("Ejecutando inferencia...")
t0 = time.perf_counter()

with torch.no_grad():
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=128,
        num_beams=3
    )

t1 = time.perf_counter()
print(f"Inferencia terminada en {t1 - t0:.2f} segundos")

print("Procesando salida...")
t0 = time.perf_counter()

generated_text = processor.batch_decode(
    generated_ids,
    skip_special_tokens=False
)[0]

parsed = processor.post_process_generation(
    generated_text,
    task=prompt,
    image_size=(image.width, image.height)
)

t1 = time.perf_counter()
print(f"Salida procesada en {t1 - t0:.2f} segundos")

fin_total = time.perf_counter()

print("\nResultado:")
print(parsed)

print(f"\nTiempo total: {fin_total - inicio_total:.2f} segundos")