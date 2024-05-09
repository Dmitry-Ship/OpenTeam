import json
from base import Agent
from .tools import upsert_mindmap, get_all_text_from_flip
from dotenv import load_dotenv
import os

load_dotenv(override=True)
MODEL = os.getenv("OPENAI_MODEL_NAME")

mindmap_creator = Agent(
    name="mindmap_creator", 
    model=MODEL,
    system_message="""
    Given a content, create a mindmap with at least 3 levels. 10 items maximum. Respond in markdown format. 
    Example:
    # Modern Psychology

    ## Branches of Psychology
    - **Clinical Psychology**
        - Psychotherapy
        - Psychological Testing
        - Mental Health Disorders
    - **Cognitive Psychology**
        - Perception
        - Memory
        - Decision Making

    ## Key Concepts
    - **Behaviorism**
        - Classical Conditioning
        - Operant Conditioning
    - **Psychoanalysis**
        - Id, Ego, and Superego
        - Defense Mechanisms
            # Artificial Intelligence
            - **Machine Learning**
                - *Supervised Learning*
                    - Classification
                    - Regression
                - *Unsupervised Learning*
                    - Clustering
                    - Association
    
    Pass the markdown to the upsert_mindmap function""",
    tools=[upsert_mindmap],
)


suggester = Agent(
    name="suggester", 
    system_message="""
    Get all texts from elements of a 2D canvas and suggest three topics for mindmaps based on them. If there is no text, suggest topics about AI.

    Respond in JSON and nothing else: 
    {
        "suggestions": ["..."]
    }
""",
    model=MODEL,
    tools=[get_all_text_from_flip],
)

