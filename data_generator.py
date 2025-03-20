import random
import datetime
import csv
from faker import Faker

fake = Faker()  # This is the api to generate fake data like email, phone no ..

random.seed(42)
fake.seed_instance(42)

NUM_DEPARTMENTS = 10
NUM_INSTRUCTORS = 100
NUM_COURSES = 200
NUM_STUDENTS = 5000
NUM_ENROLLMENTS = 20000

dept_ids = []
instructor_ids = []
course_ids = []
student_ids = []

used_instructor_emails = set()  # This set will make sure no duplicates
used_student_emails = set()

# Generate Departments
departments = []
dept_names = [
    "Computer Science", "Electronics", "Physics", "Chemistry", "Biology",
    "Mathematics", "History", "Psychology", "Business", "Electrical"
]

for i in range(NUM_DEPARTMENTS):
    dept_id = i + 1
    dept_ids.append(dept_id)
    established = fake.date_between(start_date=datetime.date(1970, 1, 1), end_date=datetime.date(2025, 3, 18))
    departments.append({
        'dept_id': dept_id,
        'dept_name': dept_names[i],
        'location': fake.building_number() + " " + fake.street_name(),
        'established': established.strftime('%Y-%m-%d')
    })

with open('departments.csv', 'w', newline='') as f:   # write to csv 
    writer = csv.DictWriter(f, fieldnames=['dept_id', 'dept_name', 'location', 'established'])
    writer.writeheader()
    writer.writerows(departments)

#Generate Instructors
instructors = []
for i in range(NUM_INSTRUCTORS):
    instructor_id = i + 1
    instructor_ids.append(instructor_id)

    dept_id = random.choice(dept_ids)
    hire_date = fake.date_between(start_date=datetime.date(1990, 1, 1), end_date=datetime.date(2025, 3, 18))


    first_name = fake.first_name()
    last_name = fake.last_name()

    email = f"{first_name}@tamu.edu"
    while email in used_instructor_emails:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name}@tamu.edu"
    used_instructor_emails.add(email)

   # phone = fake.phone_number()
    phone = fake.numerify("###-###-####")

    instructors.append({
        'instructor_id': instructor_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'dept_id': dept_id
    })

with open('instructors.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'instructor_id', 'first_name', 'last_name', 'email', 
        'phone', 'hire_date', 'dept_id'
    ])
    writer.writeheader()
    writer.writerows(instructors)

# Generate Department Heads
dept_heads = []
for dept_id in dept_ids:
    
    dept_instructors = [instr for instr in instructors if instr['dept_id'] == dept_id]
    if dept_instructors:
        head = random.choice(dept_instructors)
        start_date = fake.date_between(
            start_date=datetime.datetime.strptime(head['hire_date'], '%Y-%m-%d').date(),
            end_date=datetime.date(2025, 3, 18)
        )
        dept_heads.append({
            'dept_id': dept_id,
            'instructor_id': head['instructor_id'],
            'start_date': start_date.strftime('%Y-%m-%d')
        })

with open('department_heads.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['dept_id', 'instructor_id', 'start_date'])
    writer.writeheader()
    writer.writerows(dept_heads)

dept_courses = {}  # these are courses titles and descriptions

dept_courses[1] = {
    "titles": [
        "Introduction to Programming", "Data Structures and Algorithms", "Database Systems",
            "Computer Networks", "Operating Systems", "Software Engineering", "Artificial Intelligence",
            "Machine Learning", "Computer Graphics", "Web Development", "Mobile App Development",
            "Information Security", "Cloud Computing", "Computer Architecture", "Human-Computer Interaction",
            "Computer Vision", "Natural Language Processing", "Distributed Systems", "Quantum Computing",
            "Blockchain Technology"
    ],
    "descriptions": [
        "Introduces basic programming concepts with Python including variables, loops, and functions.",
            "Covers advanced data structures like trees, graphs, and algorithms for searching and sorting.",
            "Explores relational database design, SQL, and database management systems.",
            "Studies network protocols, architectures, and security across different network types.",
            "Examines process management, memory allocation, and file systems in modern OS.",
            "Teaches software development methodologies, testing, and project management.",
            "Introduces AI concepts including search algorithms, knowledge representation, and reasoning.",
            "Covers supervised and unsupervised learning algorithms and neural networks.",
            "Focuses on 2D and 3D rendering techniques and visualization algorithms.",
            "Teaches HTML, CSS, JavaScript and frameworks for creating modern websites.",
            "Explores native and cross-platform mobile application development.",
            "Covers cryptography, network security, and ethical hacking principles.",
            "Studies distributed computing resources and services delivered over the Internet.",
            "Examines processor design, memory hierarchies, and system architecture.",
            "Focuses on designing user interfaces and improving user experience.",
            "Explores image processing and algorithms for visual data interpretation.",
            "Studies computational techniques for analyzing and generating human language.",
            "Covers concepts and challenges in multi-computer systems.",
            "Introduces quantum algorithms and potential applications in computing.",
            "Explores distributed ledger technology and decentralized applications."
    ]
}

dept_courses[2] = {
    "titles": [
        "Circuit Analysis", "Digital Logic Design", "Microprocessors", "Analog Electronics",
            "Digital Signal Processing", "VLSI Design", "Power Electronics", "Control Systems",
            "Electronic Materials", "Embedded Systems", "PCB Design", "RF Circuit Design",
            "Optoelectronics", "Semiconductor Devices", "Automation and Controls", "Robotics",
            "Instrumentation", "Integrated Circuit Design", "MEMs and Nanotechnology", "Wireless Communication"
    ],
    "descriptions": [
         "Introduces Kirchhoff's laws and circuit analysis techniques for DC and AC circuits.",
            "Covers combinational and sequential logic circuits using gates and flip-flops.",
            "Studies architecture and programming of microprocessors and microcontrollers.",
            "Explores transistor circuits, amplifiers, and operational amplifier applications.",
            "Teaches discrete-time signal analysis, filtering, and FFT algorithms.",
            "Covers design and fabrication of integrated circuits.",
            "Studies conversion and control of electrical power using semiconductor devices.",
            "Explores automatic control systems including feedback and stability analysis.",
            "Examines properties and applications of materials used in electronic devices.",
            "Focuses on hardware-software integration in small computing systems.",
            "Teaches design and manufacturing of printed circuit boards.",
            "Covers high-frequency circuits for wireless and communication systems.",
            "Studies light-emitting and light-detecting semiconductor devices.",
            "Explores physics and operation of semiconductor electronic devices.",
            "Covers industrial automation systems and programmable logic controllers.",
            "Introduces robotic systems, sensors, actuators, and control algorithms.",
            "Studies measurement systems, sensors, and data acquisition.",
            "Focuses on design of analog, digital, and mixed-signal integrated circuits.",
            "Explores micro-electromechanical systems and nanotechnology applications.",
            "Covers modulation techniques and wireless system design principles."
    ]
}


dept_courses[3] = {
    "titles": [
        "Classical Mechanics", "Electromagnetism", "Quantum Physics", "Thermodynamics",
        "Statistical Mechanics", "Nuclear Physics", "Particle Physics", "Astrophysics",
        "Solid State Physics", "Optics", "Relativity", "Quantum Field Theory",
        "Fluid Dynamics", "Computational Physics", "Experimental Methods", "Cosmology",
        "Atomic Physics", "Plasma Physics", "Biophysics", "Mathematical Physics"
    ],
    "descriptions": [
        "Studies motion and forces using Newton's laws and Lagrangian mechanics.",
        "Explores electric and magnetic fields, Maxwell's equations, and electromagnetic waves.",
        "Introduces quantum mechanical principles and applications to atomic systems.",
        "Covers heat, energy, and thermodynamic processes and principles.",
        "Examines statistical behavior of physical systems with many particles.",
        "Studies nuclear structure, reactions, and applications of nuclear processes.",
        "Explores elementary particles, interactions, and the standard model.",
        "Applies physics principles to astronomical objects and the universe.",
        "Examines crystal structures, electronic properties, and condensed matter.",
        "Studies light propagation, lenses, and optical instruments and phenomena.",
        "Covers special and general relativity theories and their implications.",
        "Explores quantum mechanical treatment of fields and particles.",
        "Studies behavior of liquids and gases in motion and fluid properties.",
        "Teaches numerical methods for solving physics problems with computers.",
        "Covers experimental design, measurement techniques, and data analysis.",
        "Examines the origin, evolution, and structure of the universe.",
        "Studies structure and properties of atoms and their interactions with light.",
        "Explores ionized gas behavior and fusion energy principles.",
        "Applies physics principles to biological systems and processes.",
        "Covers advanced mathematical methods used in theoretical physics."
    ]
}

# Chemistry department
dept_courses[4] = {
    "titles": [
        "General Chemistry", "Organic Chemistry I", "Organic Chemistry II", "Analytical Chemistry",
        "Physical Chemistry", "Inorganic Chemistry", "Biochemistry", "Spectroscopy",
        "Environmental Chemistry", "Medicinal Chemistry", "Polymer Chemistry", "Quantum Chemistry",
        "Computational Chemistry", "Electrochemistry", "Industrial Chemistry", "Green Chemistry",
        "Nuclear Chemistry", "Organometallic Chemistry", "Surface Chemistry", "Chemical Kinetics"
    ],
    "descriptions": [
        "Introduces fundamental concepts of matter, stoichiometry, and chemical reactions.",
        "Covers structure, properties, and reactions of hydrocarbons and their derivatives.",
        "Explores advanced organic reactions, mechanisms, and synthesis strategies.",
        "Studies methods for determining chemical composition and structure.",
        "Examines theoretical principles underlying chemical phenomena.",
        "Covers chemistry of non-carbon elements, coordination compounds, and catalysis.",
        "Explores chemical processes and substances in living organisms.",
        "Studies interaction of matter with electromagnetic radiation for structural analysis.",
        "Examines chemical processes in air, water, and soil environments.",
        "Explores design and development of pharmaceutical compounds.",
        "Covers large molecules composed of repeating structural units.",
        "Studies application of quantum mechanics to molecular structure and spectra.",
        "Explores computer modeling of molecular properties and reactions.",
        "Studies chemical reactions involving electron transfer.",
        "Covers large-scale chemical production processes and economics.",
        "Explores design of chemical products and processes to reduce environmental impact.",
        "Studies radioactive decay, nuclear reactions, and applications.",
        "Covers compounds containing bonds between carbon and metals.",
        "Examines chemical processes on surfaces and interfaces.",
        "Studies rates of chemical reactions and reaction mechanisms."
    ]
}

# Biology department
dept_courses[5] = {
    "titles": [
        "Cell Biology", "Genetics", "Ecology", "Evolution", "Microbiology",
        "Anatomy and Physiology", "Molecular Biology", "Botany", "Zoology", "Immunology",
        "Neurobiology", "Developmental Biology", "Marine Biology", "Biotechnology",
        "Virology", "Entomology", "Conservation Biology", "Parasitology", "Mycology", "Bioinformatics"
    ],
    "descriptions": [
        "Studies structure and function of cells as the basic units of life.",
        "Explores inheritance, genes, and genetic variation in organisms.",
        "Examines relationships between organisms and their environment.",
        "Studies changes in species over time and mechanisms of natural selection.",
        "Explores microscopic organisms including bacteria, viruses, and fungi.",
        "Covers structure and function of body systems and organs.",
        "Studies biomolecules and their interactions in cellular processes.",
        "Explores plant structure, physiology, ecology, and classification.",
        "Examines animal diversity, behavior, physiology, and evolution.",
        "Studies immune system function, disorders, and responses to pathogens.",
        "Explores structure and function of the nervous system.",
        "Examines processes by which organisms grow and develop.",
        "Studies organisms living in marine environments and ecosystems.",
        "Covers applications of biology in technology and industry.",
        "Explores viral structure, replication, and virus-host interactions.",
        "Studies insects, their biology, ecology, and impacts on humans.",
        "Examines preservation of biodiversity and endangered species.",
        "Studies parasitic organisms and their relationships with hosts.",
        "Explores fungi biology, diversity, and ecological roles.",
        "Applies computational methods to biological data analysis."
    ]
}

# Mathematics department
dept_courses[6] = {
    "titles": [
        "Calculus I", "Calculus II", "Linear Algebra", "Differential Equations", "Abstract Algebra",
        "Real Analysis", "Complex Analysis", "Number Theory", "Topology", "Numerical Analysis",
        "Probability Theory", "Mathematical Statistics", "Discrete Mathematics", "Graph Theory",
        "Cryptography", "Optimization", "Game Theory", "Combinatorics", "Differential Geometry", "Functional Analysis"
    ],
    "descriptions": [
        "Introduces limits, derivatives, and applications of differential calculus.",
        "Explores integration techniques, sequences, series, and applications.",
        "Covers vector spaces, matrices, and linear transformations.",
        "Studies methods for solving differential equations and their applications.",
        "Explores algebraic structures including groups, rings, and fields.",
        "Covers rigorous treatment of the real number system and calculus.",
        "Explores functions of complex variables and their properties.",
        "Studies properties of integers and related structures.",
        "Examines properties of spaces preserved under continuous deformations.",
        "Covers algorithms for approximating mathematical problems.",
        "Explores random phenomena, probability spaces, and distributions.",
        "Studies statistical inference, estimation, and hypothesis testing.",
        "Covers mathematical structures that are fundamentally discrete.",
        "Studies properties of graphs and their applications to networks.",
        "Explores mathematical techniques for secure communication.",
        "Studies methods for finding maximum or minimum values of functions.",
        "Explores mathematical modeling of strategic interactions.",
        "Studies counting, arrangement, and existence questions for finite sets.",
        "Explores curves, surfaces, and their properties using calculus.",
        "Studies infinite-dimensional vector spaces and operators."
    ]
}

# History department
dept_courses[7] = {
    "titles": [
        "World History", "American History", "European History", "Asian History", "Ancient Civilizations",
        "Medieval History", "Renaissance and Reformation", "Modern History", "Military History", "Economic History",
        "Social History", "Cultural History", "History of Science", "Political History", "Environmental History",
        "Women's History", "African History", "Latin American History", "Middle Eastern History", "Historiography"
    ],
    "descriptions": [
        "Surveys major developments in global history from ancient times to present.",
        "Explores political, social, and cultural development of the United States.",
        "Studies major events and trends in European history.",
        "Examines historical developments in East, South, and Southeast Asia.",
        "Explores early civilizations including Mesopotamia, Egypt, Greece, and Rome.",
        "Studies European history from the fall of Rome to the Renaissance.",
        "Examines European cultural and religious developments from 14th-17th centuries.",
        "Covers major historical developments from the 18th century to present.",
        "Studies warfare and military institutions throughout history.",
        "Explores economic systems, trade, and development in historical context.",
        "Examines everyday life, social classes, and community structures in history.",
        "Studies cultural expressions, beliefs, and practices throughout history.",
        "Explores development of scientific knowledge and institutions over time.",
        "Studies governmental systems and political movements throughout history.",
        "Examines human interaction with the natural environment over time.",
        "Explores women's experiences, contributions, and gender relations in history.",
        "Studies historical developments across the African continent.",
        "Examines history of Central and South America and the Caribbean.",
        "Explores historical developments across the Middle East and North Africa.",
        "Studies historical methods, interpretation, and the writing of history."
    ]
}

# Psychology department
dept_courses[8] = {
    "titles": [
        "Introduction to Psychology", "Cognitive Psychology", "Social Psychology", "Developmental Psychology",
        "Abnormal Psychology", "Clinical Psychology", "Personality Psychology", "Neuropsychology",
        "Health Psychology", "Industrial-Organizational Psychology", "Educational Psychology", "Experimental Psychology",
        "Sensation and Perception", "Learning and Memory", "Motivation and Emotion", "Psychopharmacology",
        "Psychotherapy", "Cultural Psychology", "Evolutionary Psychology", "Positive Psychology"
    ],
    "descriptions": [
        "Surveys major areas of psychology including cognition, development, and behavior.",
        "Studies mental processes including attention, memory, problem solving, and decision making.",
        "Explores how people's thoughts, feelings, and behaviors are influenced by others.",
        "Examines psychological development across the lifespan.",
        "Studies psychological disorders, their causes, and treatments.",
        "Explores assessment and treatment of psychological disorders.",
        "Studies individual differences in patterns of thinking, feeling, and behaving.",
        "Examines relationships between brain function and psychological processes.",
        "Explores psychological factors in health, illness, and healthcare.",
        "Studies workplace behavior, organizations, and personnel psychology.",
        "Examines psychological principles applied to educational issues.",
        "Covers research methods used to study psychological phenomena.",
        "Studies how we detect and interpret sensory information from our environment.",
        "Explores processes of acquiring, storing, and retrieving information.",
        "Examines factors that direct and energize behavior.",
        "Studies effects of drugs on psychological processes and behavior.",
        "Explores various approaches to psychological treatment and counseling.",
        "Studies cultural factors in psychological processes across different societies.",
        "Examines psychological traits as evolved adaptations.",
        "Explores strengths, well-being, and optimal human functioning."
    ]
}

# Business department
dept_courses[9] = {
    "titles": [
        "Principles of Management", "Marketing Fundamentals", "Financial Accounting", "Business Ethics",
        "Organizational Behavior", "Corporate Finance", "Strategic Management", "Entrepreneurship",
        "Human Resource Management", "Operations Management", "International Business", "Business Law",
        "Supply Chain Management", "Business Analytics", "Consumer Behavior", "Financial Markets",
        "Digital Marketing", "Project Management", "Business Communication", "Risk Management"
    ],
    "descriptions": [
        "Introduces fundamental management concepts, functions, and skills.",
        "Covers core marketing principles, consumer needs, and marketing strategies.",
        "Introduces accounting principles for recording and reporting financial information.",
        "Explores ethical issues and decision-making in business contexts.",
        "Studies human behavior in organizational settings.",
        "Explores financial decision-making within business organizations.",
        "Studies formulation and implementation of organizational objectives and strategies.",
        "Covers starting and managing new business ventures.",
        "Explores practices for effectively managing an organization's workforce.",
        "Studies production and delivery of goods and services.",
        "Examines business conducted across national boundaries.",
        "Covers legal principles affecting business operations and decisions.",
        "Studies management of materials and information flows in organizations.",
        "Explores data analysis for business decision-making.",
        "Studies factors influencing consumer purchasing decisions.",
        "Explores organization and functioning of financial systems.",
        "Covers online marketing strategies and tools.",
        "Studies planning, organizing, and managing resources for project completion.",
        "Explores effective communication in business contexts.",
        "Covers identification, assessment, and management of business risks."
    ]
}

# Electrical department
dept_courses[10] = {
    "titles": [
        "Electric Circuits", "Electromagnetic Fields", "Electronic Devices", "Digital Systems",
        "Power Systems", "Communication Systems", "Control Engineering", "Signal Processing",
        "Microelectronics", "Electric Machines", "Power Electronics", "High Voltage Engineering",
        "Renewable Energy Systems", "Electric Drives", "Digital Communication", "Antenna Theory",
        "VLSI Design", "Embedded Systems", "Computer Architecture", "Smart Grid Technology"
    ],
    "descriptions": [
        "Introduces principles of electric circuit analysis and design.",
        "Studies electric and magnetic fields and their engineering applications.",
        "Explores semiconductor devices and their applications in circuits.",
        "Covers design and analysis of digital logic circuits and systems.",
        "Studies generation, transmission, and distribution of electrical power.",
        "Explores principles and systems for transmitting information.",
        "Covers analysis and design of control systems for dynamic processes.",
        "Explores processing and analysis of signals in electrical systems.",
        "Studies design and fabrication of electronic components at microscale.",
        "Covers principles of electromechanical energy conversion devices.",
        "Studies conversion and control of electric power using electronic devices.",
        "Explores insulation requirements and testing for high voltage systems.",
        "Covers solar, wind, and other renewable electrical generation systems.",
        "Studies electric motors and their control systems.",
        "Explores digital transmission of information in communication systems.",
        "Studies radiation, design, and application of antennas.",
        "Covers design of very large scale integrated circuits.",
        "Explores computer systems embedded in larger mechanical or electronic systems.",
        "Studies design and organization of computer processors and systems.",
        "Explores integration of advanced technologies in electrical power grids."
    ]
}


courses = []
course_prefixes = {
    1: "CSE", 2: "ECE", 3: "PHYS", 4: "CHEM", 5: "BIO",
    6: "MATH", 7: "HIST", 8: "PSYCH", 9: "BUSI", 10: "EE"
}
used_course_codes = set()


for i in range(NUM_COURSES):
    course_id = i + 1
    course_ids.append(course_id)

    dept_id = i//20 + 1
    
    dept_instructors_ids = [
        instr['instructor_id'] for instr in instructors if instr['dept_id'] == dept_id
    ]
    instructor_id = random.choice(dept_instructors_ids)

    # Unique code
    code_unique = False
    while not code_unique:
        number = random.randint(400, 799)
        course_code = f"{course_prefixes[dept_id]}{number}"
        if course_code not in used_course_codes:
            used_course_codes.add(course_code)
            code_unique = True

    credits = random.choice([1, 2, 3, 4])

    courses.append({
        'course_id': course_id,
        'course_code': course_code,
        'title': dept_courses[dept_id]["titles"][i%20],
        'credits': credits,
        'description': dept_courses[dept_id]["descriptions"][i%20],
        'dept_id': dept_id,
        'instructor_id': instructor_id
    })

with open('courses.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'course_id', 'course_code', 'title', 'credits', 
        'description', 'dept_id', 'instructor_id'
    ])
    writer.writeheader()
    writer.writerows(courses)

# Generate Students
students = []
majors = dept_names + [
    f"{dept_names[i]} & {dept_names[j]}"
    for i in range(len(dept_names))
    for j in range(i+1, len(dept_names))
    if j < i+3
]

for i in range(NUM_STUDENTS):
    student_id = i + 1
    student_ids.append(student_id)

    enrollment_date = fake.date_between(
        start_date=datetime.date(2021, 1, 1), 
        end_date=datetime.date(2025, 3, 18)
    )

    # Ensure unique email
    first_name = fake.first_name()
    last_name = fake.last_name()

    email = f"{first_name}{last_name}@tamu.edu"
    while email in used_student_emails:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name}{last_name}@tamu.edu"
    used_student_emails.add(email)

    students.append({
        'student_id': student_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'enrollment_date': enrollment_date.strftime('%Y-%m-%d'),
        'major': random.choice(majors)
    })

with open('students.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'student_id', 'first_name', 'last_name', 'email', 
        'enrollment_date', 'major'
    ])
    writer.writeheader()
    writer.writerows(students)

# Generate Enrollments (no duplicates)
enrollments = set()
possible_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F', 'W', 'I']

while len(enrollments) < NUM_ENROLLMENTS:
    st_id = random.choice(student_ids)
    crs_id = random.choice(course_ids)
    if (st_id, crs_id) not in enrollments:
        enrollments.add((st_id, crs_id))

enrollment_records = []
for (st_id, crs_id) in enrollments:
    enrollment_date = fake.date_between(
        start_date=datetime.date(2021, 1, 1), 
        end_date=datetime.date(2025, 3, 18)
    )
    
    grade = random.choice(possible_grades) if random.random() < 0.8 else None

    enrollment_records.append({
        'student_id': st_id,
        'course_id': crs_id,
        'enrollment_date': enrollment_date.strftime('%Y-%m-%d'),
        'grade': grade
    })

with open('enrollments.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'student_id', 'course_id', 'enrollment_date', 'grade'
    ])
    writer.writeheader()
    writer.writerows(enrollment_records)

print(f"Generated data files:")
print(f"- {len(departments)} departments")
print(f"- {len(instructors)} instructors")
print(f"- {len(dept_heads)} department heads")
print(f"- {len(courses)} courses")
print(f"- {len(students)} students")
print(f"- {len(enrollment_records)} enrollments")
