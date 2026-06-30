import shutil
import subprocess
import sys
import time
import urllib.request
import json


OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"


def run(command):
    subprocess.run(command, check=True)


def install_requirements():
    print("Installing Python dependencies...")
    run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def is_ollama_installed():
    return shutil.which("ollama") is not None


def is_ollama_running():
    try:
        urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3)
        return True
    except Exception:
        return False


def start_ollama():
    print("Starting Ollama...")
    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for _ in range(20):
        if is_ollama_running():
            print("Ollama is running.")
            return
        time.sleep(1)

    raise RuntimeError("Failed to start Ollama.")


def get_ollama_models():
    response = urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=10)
    data = json.loads(response.read().decode("utf-8"))
    return [model["name"] for model in data.get("models", [])]


def ensure_ollama():
    print("Checking Ollama...")

    if not is_ollama_installed():
        raise RuntimeError(
            "Ollama is not installed. Install it first with: brew install ollama"
        )

    if not is_ollama_running():
        start_ollama()

    models = get_ollama_models()

    if OLLAMA_MODEL not in models:
        print(f"Downloading model: {OLLAMA_MODEL}")
        run(["ollama", "pull", OLLAMA_MODEL])
    else:
        print(f"Model ready: {OLLAMA_MODEL}")


def main():
    install_requirements()
    ensure_ollama()

    print("Starting job-agent...")
    run([sys.executable, "main.py"])


if __name__ == "__main__":
    main()