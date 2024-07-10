<!-- # AI-Agent
AI-Agent , client offert generator

# Salut! Numele meu este Alin Dobrea.
# Nivel de experiență = Începător

Am decis să folosesc LLM-ul, Gemma 2. llama3 nu interacționează foarte bine cu limba română și rezultă în mai multe erori/halucinații.

De asemenea, voi folosi CrewAi, pentru antrenarea și configurarea agenților AI.

# Here we go..

Am început prin conversia fișierelor cu oferte din .docx în .pdf , în felul acesta, LLM-ul poate citi cu ușurință fișierul mulțumită modulului (pdfminer.high_level).

Prin urmare, începem cu primul modul. -->

from pdfminer.high_level import extract_text

<!-- mai departe, importăm Ollama și CrewAi -->

from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

<!-- vom folosi modelul Gemma2: 9b -->

model = Ollama(model = "gemma2:9b")