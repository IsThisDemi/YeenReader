# YeenReader

Un assistente AI che legge manuali PDF e risponde alle domande citando i riferimenti.

## Requisiti
- Python 3.9+
- [Ollama](https://ollama.com/) installato e in esecuzione
- Modello Ollama (es. `mistral`) scaricato

## Installazione
1. Crea e attiva un ambiente virtuale:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. Installa le dipendenze:
   ```powershell
   pip install -r requirements.txt
   pip install langchain-huggingface langchain-ollama langchain-community pypdf pymupdf sentence-transformers faiss-cpu
   ```
3. (Facoltativo) Scarica il modello Ollama desiderato:
   ```powershell
   ollama pull mistral
   ```

## Utilizzo
1. Copia un manuale PDF nella cartella del progetto (es. `manuale.pdf`).
2. Indicizza il manuale:
   ```powershell
   python manual_reader.py manuale.pdf
   ```
3. Fai una domanda:
   ```powershell
   python manual_reader.py manuale.pdf query "Come aggiornare il telefono?"
   ```
   Oppure:
   ```powershell
   python manual_reader.py manuale.pdf query
   # poi inserisci la domanda da tastiera
   ```

## Note
- Il modello di default è `mistral`. Puoi modificarlo nel codice.
- Funziona anche con altri modelli Ollama (es. qwen3, gemma, llama2).
- I chunk e l'indice sono salvati in `faiss_index/`.

## Esclusioni
Vedi `.gitignore` per i file esclusi dal controllo versione.
