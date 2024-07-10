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

<!-- mai departe, instalăm și importăm Ollama și CrewAi -->

//terminal//
pip install crewai
ollama run gemma2
//terminal//

from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

<!-- vom folosi modelul Gemma2: 9b -->

model = Ollama(model = "gemma2:9b")

<!-- Cerem un prompt pentru AI pentru a stabili ce tip de business are nevoie client-ul. -->

salut = "Salut! Spune ce tip de afacere iti doresti!"
prompt = input(salut)

<!-- Train thought:

Am încercat să creez un agent care să citească fișierele, și să analizeze structura/layout-ul documentelor.
Din oarecare motiv, acesta reușea să extragă corect doar ultimele 2 sub-capitole (Probabil datorită redactării documentului).
Așa că.. m-am dat bătut și am creat un fișier PDF în care i-am scris concis structura fișierului, respectiv:

    1 - Scopul Documentului:
    2 - Propunere structura:
    3 - Sugestii suplimentare:
    4 - Pret si timp de implementare: -->

struc = extract_text("structura.pdf")

reader = Agent(
    role = "Reader",
    goal = """Your goal is to read the file and to understand the structure of the file. You have to see the chapters/structure and to give your agent co-workers the exact framework so they can respect it, when building further projects.""",
    backstory = "You're an expert document analyzer.",
    verbose = True,
    allow_delegation = False,
    llm = model
)

task = Task(
    description = f"""Read file: {struc}, and create a model for other agents to follow, each chapter should keep it's name and it should be created into a future model for other offers.""",
    agent = reader,
    expected_output = "Write in Romanian language.A model for future offers, respecting the structure of the initial document."
)

<!-- Acest agent acum va avea rolul de a citi documentul cu structura și de a o prezenta celorlalți agenți AI. -->


<!-- Apoi am încercat să creez un agent care să citească fișierele cu oferte și să înțeleagă despre ce este vorba în document, ce relevanță are fiecare sub-capitol și să-l asocieze cu paragraful din care face parte. -->

reader2 = Agent(
    role = "Analyzer",
    goal = """Your goal is to read the documents and understand what the document is about, you need to analyze all the chapters of the document and you need to associate each answer with it's title/subtitle.""",
    backstory = "You're an expert document analyzer.",
    verbose = True,
    allow_delegation = False,
    llm = model
)

task2 = Task(
    description = f"""Read text: {text1} and {text2}, and use the model from agent 'Reader' to populate the sub-chapters with answers.
    You need to respect the model by 'Reader' and you need to add the chapters and answers according to what you find in the documents.""",
    agent = reader2,
    expected_output = "Write in Romanian language.A report"
)

<!-- Iar in final, am creat un agent care analizeaza prompt-ul clientului si asambleaza cu ajutorul colegilor sai un raport cu structura ofertelor din exemple. -->

expert = Agent(
    role = "Expert Software Developer",
    goal = """Your goal is to analyze the request of the user and to think about every single detail that we would need to implement in order to create this project.
    For example, you need to think about all the required technologies, all the required programming languages,
    all the required tasks for developing the application, etc.""",
    backstory = "You're an expert software developer..",
    verbose = True,
    allow_delegation = False,
    llm = model
)

task3 = Task(
    description = f"""Modelul de afaceri al clientului este: {prompt}. 
    Va rugam sa analizati acest tip de afacere si sa determinati ce aplicatie are nevoie, ce tehnologii sunt necesare pentru dezvoltarea acestei aplicatii. 
    Completati structura celorlalti agenti: 'Reader' si 'Analyzer',
      si completati acele modele cu raspunsurile dvs., cum ar fi durata proiectului, tehnologiile necesare, limbajele de programare necesare, structura recomandata, sugestii suplimentare, pretul, etc. 
      De asemenea, asigurati-va ca adaugati sarcinile care nu sunt mentionate de utilizator, dar care sunt totusi necesare, 
      cum ar fi sectiunea financiara, metode de plata, generarea automata a facturilor, si posibilitatea pentru cumparator de a descarca factura, etc.

Creati raportul cu urmatoarea structura:
    
    1 - Scopul Documentului:
    definitii limbaje de programare, etc
    2 - Propunere structura:
    3 - Sugestii suplimentare:
    4 - Pret si timp de implementare:
    
    
    In rest, foloseste rezultatele agentilor 'Analyzer' si 'Reader' pentru a respecta structura documentelor analizate.""",
    agent = expert,
    expected_output = "Write in Romanian language.A full report of the offer"
)


<!-- Am finalizat prin a asambla crew-ul conform CrewAi și prin a printa output-ul. -->

crew = Crew(
    agents = [reader,reader2,expert],
    tasks = [task,task2,task3],
    verbose = 2,
    process = Process.sequential

)

output = crew.kickoff()
print(output)

<!-- Rezultatul nu este exact ca în exemplu, dar cu mai mult timp alocat pentru fine-tunning, cu siguranță reușim să ajungem la rezultatul dorit! 

Vă mulțumesc! -->