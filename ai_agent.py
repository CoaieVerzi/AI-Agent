from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from pdfminer.high_level import extract_text

model = Ollama(model = "gemma2:9b")
struc = extract_text("structura.pdf")
text1 = extract_text("1.pdf")
text2 = extract_text("2.pdf")

salut = "Salut! Spune ce tip de afacere iti doresti!"
prompt = input(salut)






reader = Agent(
    role = "Reader",
    goal = """Your goal is to read the file and to understand the structure of the file. You have to see the chapters/structure and to give your agent co-workers the exact framework so they can respect it, when building further projects.""",
    backstory = "You're an expert document analyzer.",
    verbose = True,
    allow_delegation = False,
    llm = model
)

reader2 = Agent(
    role = "Analyzer",
    goal = """Your goal is to read the documents and understand what the document is about, you need to analyze all the chapters of the document and you need to associate each answer with it's title/subtitle.""",
    backstory = "You're an expert document analyzer.",
    verbose = True,
    allow_delegation = False,
    llm = model
)

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


task = Task(
    description = f"""Read file: {struc}, and create a model for other agents to follow, each chapter should keep it's name and it should be created into a future model for other offers.""",
    agent = reader,
    expected_output = "Write in Romanian language.A model for future offers, respecting the structure of the initial document."
)

task2 = Task(
    description = f"""Read text: {text1} and {text2}, and use the model from agent 'Reader' to populate the sub-chapters with answers.
    You need to respect the model by 'Reader' and you need to add the chapters and answers according to what you find in the documents.""",
    agent = reader2,
    expected_output = "Write in Romanian language.A report"
)

task3 = Task(
    description = f"""Modelul de afaceri al clientului este: {prompt}. 
    Va rugam sa analizati acest tip de afacere si sa determinati ce aplicatie are nevoie, ce tehnologii sunt necesare pentru dezvoltarea acestei aplicatii. 
    Completati structura celorlalti agenti ai dvs., cei creati de 'Reader' si 'Analyzer',
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




crew = Crew(
    agents = [reader,reader2,expert],
    tasks = [task,task2,task3],
    verbose = 2,
    process = Process.sequential

)

output = crew.kickoff()
print(output)