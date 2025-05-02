import spacy
from typing import List, Dict, Any
import re

# Load English language model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model is not found, download it
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

async def analyze_feature(feature_description: str, project_id: int) -> List[Dict[str, Any]]:
    """
    Analyze a feature description and break it down into tasks.
    
    Args:
        feature_description: A string describing the feature
        project_id: The ID of the project this feature belongs to
    
    Returns:
        A list of task dictionaries with title and description
    """
    # Process the text with spaCy
    doc = nlp(feature_description)
    
    # Extract main tasks based on sentence structure
    tasks = []
    
    # Split into sentences
    sentences = list(doc.sents)
    
    # Process each sentence
    for sent in sentences:
        # Skip very short sentences (likely not tasks)
        if len(sent.text.split()) < 3:
            continue
        
        # Extract the main verb phrase and its object
        main_verb = None
        main_object = None
        
        for token in sent:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                main_verb = token
                
                # Find the direct object
                for child in token.children:
                    if child.dep_ == "dobj":
                        main_object = child
                        break
        
        if main_verb:
            # Create task title
            title = str(sent).strip()
            
            # Create more detailed description
            description = f"Extracted from feature description: {sent.text}
"
            if main_object:
                description += f"
Main action: {main_verb}
Target: {main_object}"
            
            tasks.append({
                "title": title,
                "description": description,
                "project_id": project_id,
                "status": "TODO",
                "priority": "MEDIUM"
            })
    
    # If no tasks were extracted, create a generic task
    if not tasks:
        tasks.append({
            "title": "Implement " + re.sub(r"\s+", " ", feature_description[:50]).strip() + "...",
            "description": feature_description,
            "project_id": project_id,
            "status": "TODO",
            "priority": "MEDIUM"
        })
    
    return tasks
